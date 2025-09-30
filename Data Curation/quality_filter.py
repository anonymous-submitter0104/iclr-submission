import argparse
import os
import pathlib
import time
import json
import torch
import cudf
import pandas as pd
import dask.dataframe as dd
from dask.distributed import Client
from nemo_curator.classifiers import QualityClassifier
from nemo_curator.datasets import DocumentDataset
from nemo_curator.utils.distributed_utils import get_client

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
TEXT_FIELD = "text"
BATCH_SIZE = 1000


def initialize_quality_classifier():
    print("Initializing QualityClassifier...")
    return QualityClassifier(text_field=TEXT_FIELD)


def ensure_directory_exists(directory):
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)


def log_gpu_memory():
    print(torch.cuda.memory_summary())


def quality_filter(batch_data: pd.DataFrame, quality_classifier: QualityClassifier) -> pd.DataFrame:
    try:
        start = time.time()
        ddf = dd.from_pandas(batch_data, npartitions=1)
        dataset = DocumentDataset(ddf)
        torch.cuda.empty_cache()
        log_gpu_memory()
        with torch.amp.autocast(device_type="cuda"):
            predictions_dataset = quality_classifier(dataset)
        predictions_df = predictions_dataset.df.compute()
        if hasattr(predictions_df, "to_pandas"):
            predictions_df = predictions_df.to_pandas()
        quality_values = predictions_df.iloc[:, -1].values
        batch_data["quality_pred"] = quality_values
        print(f"Quality classification completed in {time.time() - start:.2f}s")
        return batch_data
    except Exception as e:
        print(f"Error in quality filter: {str(e)}")
        raise e


def save_batch_by_quality(batch_df: pd.DataFrame, file_name: str, output_base_path: str):
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    for quality in ["High", "Medium", "Low"]:
        quality_mask = batch_df["quality_pred"] == quality
        if quality_mask.any():
            quality_df = batch_df[quality_mask]
            quality_dir = os.path.join(output_base_path, quality.upper())
            ensure_directory_exists(quality_dir)
            output_file = f"{base_name}.jsonl"
            output_path = os.path.join(quality_dir, output_file)
            with open(output_path, "a", encoding="utf-8") as f:
                quality_df.to_json(f, orient="records", lines=True, force_ascii=False)
            print(f"Saved {len(quality_df)} {quality} quality records to {output_path}")


def count_output_lines(output_base_path, base_name):
    print(f"Counting lines in output files for {base_name}...")
    total_lines = 0
    for quality in ["HIGH", "MEDIUM", "LOW"]:
        output_file = os.path.join(output_base_path, quality, f"{base_name}.jsonl")
        try:
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    total_lines += sum(1 for _ in f)
        except Exception as e:
            print(f"Error counting lines in output file {output_file}: {str(e)}")
    return total_lines


def count_lines_in_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return sum(1 for _ in f)
    except Exception as e:
        print(f"Error counting lines in file {file_path}: {str(e)}")
        return 0


def process_chunk(file_path: str, quality_classifier: QualityClassifier, output_base_path: str, client: Client):
    print(f"\nProcessing file: {file_path}")
    
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Count lines already processed in output files
    lines_processed = count_output_lines(output_base_path, base_name)
    
    try:
        total_lines = count_lines_in_file(file_path)
        if lines_processed >= total_lines:
            print(f"File {file_path} already fully processed ({lines_processed}/{total_lines} lines). Skipping.")
            return
        
        print(f"Resuming file {file_path} from line {lines_processed}/{total_lines}")
        
        # Read the file in chunks to process from where we left off
        chunk_size = 10000  # Adjust based on memory constraints
        current_line = 0
        futures = []
        
        with open(file_path, 'r') as f:
            chunk_data = []
            for i, line in enumerate(f):
                if i < lines_processed:
                    continue
                
                try:
                    json_obj = json.loads(line)
                    chunk_data.append(json_obj)
                    current_line = i + 1
                    
                    if len(chunk_data) >= chunk_size:
                        chunk_df = pd.DataFrame(chunk_data)
                        print(f"Submitting batch from line {current_line - len(chunk_data) + 1} to {current_line}")
                        futures.append(client.submit(
                            process_partition, 
                            chunk_df, 
                            quality_classifier, 
                            file_path, 
                            output_base_path
                        ))
                        
                        # Reset for next chunk
                        chunk_data = []
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON at line {i+1}: {str(e)}")
                    continue
            
            # Process the remaining chunk if any
            if chunk_data:
                chunk_df = pd.DataFrame(chunk_data)
                print(f"Submitting final batch from line {current_line - len(chunk_data) + 1} to {current_line}")
                futures.append(client.submit(
                    process_partition, 
                    chunk_df, 
                    quality_classifier, 
                    file_path, 
                    output_base_path
                ))
        
        # Wait for all futures to complete
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Error in batch processing: {str(e)}")
        
        print(f"Completed processing file {file_path}: {current_line}/{total_lines} lines")
        
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")


def process_partition(batch_df: pd.DataFrame, quality_classifier: QualityClassifier, file_path: str, output_base_path: str):
    try:
        processed_batch = quality_filter(batch_df, quality_classifier)
        save_batch_by_quality(processed_batch, file_path, output_base_path)
        return len(batch_df)
    except Exception as e:
        print(f"Error processing partition from file {file_path}: {str(e)}")
        return 0


def process_files(input_file: str, output_base_path: str, range_start: int, range_end: int):
    print("Initializing Dask Client...")
    client = get_client(cluster_type="gpu",protocol="tcp")
    client.run(lambda: print("Dask worker initialized."))
    quality_classifier = initialize_quality_classifier()
    ensure_directory_exists(output_base_path)
    
    with open(input_file, "r") as f:
        file_paths = [line.strip() for line in f if line.strip()]
    print(f"Found {len(file_paths)} files to process.")
    
    # Select files within the specified range
    file_paths_to_process = file_paths[range_start - 1 : range_end]

    for idx, file_path in enumerate(file_paths_to_process, range_start):
        print(f"\nProcessing file {idx}/{len(file_paths)}: {file_path}")
        try:
            process_chunk(file_path, quality_classifier, output_base_path, client)
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            continue
    
    client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process multiple JSONL files with quality classification")
    parser.add_argument("--input-list", type=str, required=True, help="Path to file containing list of JSONL files to process (one path per line)")
    parser.add_argument("--output-dir", type=str, default="/workspace/ajay/filtered_output", help="Base directory for output files")
    parser.add_argument("--range-start", type=int, required=True, help="Start of the range (inclusive)")
    parser.add_argument("--range-end", type=int, required=True, help="End of the range (inclusive)")
    args = parser.parse_args()

    start = time.time()
    process_files(args.input_list, args.output_dir, args.range_start, args.range_end)
    end = time.time()
    print(f"Total time taken: {end - start:.2f}s")

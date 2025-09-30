import argparse
import time
import hashlib
import json
import os
import codecs
from pathlib import Path

# Remove GPU environment variable if not needed for processing
# os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3,4,5,6,7"

def get_all_files_paths_under(directory):
    """
    Get all file paths under a directory recursively.
    Replacement for nemo_curator's get_all_files_paths_under.
    """
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.jsonl') or file.endswith('.json'):
                file_paths.append(os.path.join(root, file))
    return file_paths

def load_file_paths_from_txt(file_list_path):
    """
    Load file paths from a text file, one path per line.
    """
    file_paths = []
    with codecs.open(file_list_path, 'r', encoding='utf-8') as f:
        for line in f:
            file_path = line.strip()
            if file_path and os.path.exists(file_path):
                file_paths.append(file_path)
            elif file_path:
                print(f"Warning: File not found: {file_path}")
    return file_paths

def compute_hash(record, hash_algorithm='md5'):
    """
    Compute the hash of the 'text' attribute of the given record (JSON-like dict).
    Ensures proper handling of Hindi text.
    """
    # Extract the 'text' attribute from the record
    text = record.get('text', '')  # Default to empty string if 'text' is not found
    if not text:
        print(f"Warning: Missing 'text' attribute in record, skipping hash computation.")
        return None

    # Normalize Hindi text and compute hash
    # Using UTF-8 encoding to preserve Hindi characters
    normalized_text = text.strip()  # Remove leading/trailing whitespace
    hash_object = hashlib.new(hash_algorithm, normalized_text.encode('utf-8'))
    record_hash = hash_object.hexdigest()
    return record_hash

def create_output_path(input_file, output_base_dir, use_flat_structure=False):
    """
    Create output path. If use_flat_structure is True, use just the filename.
    Otherwise, try to preserve some directory structure.
    """
    input_path = Path(input_file)
    
    if use_flat_structure:
        # Just use the filename
        return str(Path(output_base_dir) / input_path.name)
    else:
        # Try to preserve some structure using parent directory name
        parent_name = input_path.parent.name
        return str(Path(output_base_dir) / parent_name / input_path.name)

def process_file(input_file, output_base_dir, processed_hashes_file, existing_hashes, output_batch_size=10000, hash_batch_size=5000, hash_algorithm='md5', use_flat_structure=False):
    """
    Process each JSONL file and write non-duplicate records to output in batches.
    Ensures Hindi text is properly handled.
    """
    print(f"Processing file: {input_file}")
    processed_count = 0
    duplicate_count = 0
    batch_records = []
    hash_batch = []
    
    # Create output file path
    output_file_path = create_output_path(input_file, output_base_dir, use_flat_structure)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    
    # Open input file with UTF-8 encoding to support Hindi characters
    with codecs.open(input_file, 'r', encoding='utf-8') as infile, \
         codecs.open(output_file_path, 'w', encoding='utf-8') as outfile:
        
        for line_num, line in enumerate(infile, 1):
            try:
                # Attempt to parse the JSON line
                record = json.loads(line.strip())
            except json.JSONDecodeError as e:
                # Skip problematic lines and log the issue
                print(f"Error decoding JSON on line {line_num} in {input_file}: {e}. Skipping this line.")
                continue

            # Compute hash and process the record
            record_hash = compute_hash(record, hash_algorithm)

            if record_hash and record_hash not in existing_hashes:
                # If hash is unique, add it to the existing_hashes set and add the record to the batch
                existing_hashes.add(record_hash)
                
                # Preserve original record with all attributes intact
                batch_records.append(json.dumps(record, ensure_ascii=False))  # Preserve non-ASCII characters
                hash_batch.append(record_hash)

                processed_count += 1
            else:
                duplicate_count += 1

            # Write hash batch when batch size is reached
            if len(hash_batch) >= hash_batch_size:
                processed_hashes_file.write('\n'.join(hash_batch) + '\n')
                processed_hashes_file.flush()
                hash_batch = []

            # Write output batch when batch size is reached
            if len(batch_records) >= output_batch_size:
                outfile.write('\n'.join(batch_records) + '\n')
                outfile.flush()
                batch_records = []

            # Print progress for every 100000 records processed
            if line_num % 100000 == 0:
                print(f"Processed {line_num} records in {input_file} ({processed_count} unique, {duplicate_count} duplicates).")

        # Write any remaining records and hashes
        if batch_records:
            outfile.write('\n'.join(batch_records) + '\n')
            outfile.flush()
            
        if hash_batch:
            processed_hashes_file.write('\n'.join(hash_batch) + '\n')
            processed_hashes_file.flush()

    print(f"Finished processing {input_file}. {processed_count} unique records written to {output_file_path}. {duplicate_count} duplicates found.\n")
    return processed_count, duplicate_count

def main(args):
    
    output_base_dir = args.output_dir
    processed_hashes_file_path = args.hash_file
    skipped_files_log_path = args.log_file
    
    print("Starting deduplication.....")
    
    # Load file paths from input sources
    all_files = []
    
    if args.file_list:
        # If file_list contains actual file paths
        for file_path in args.file_list:
            if os.path.isfile(file_path):
                # It's a single file
                if file_path.endswith('.jsonl') or file_path.endswith('.json'):
                    all_files.append(file_path)
                else:
                    # It's a text file containing list of file paths
                    print(f"Loading file paths from: {file_path}")
                    file_list = load_file_paths_from_txt(file_path)
                    all_files.extend(file_list)
                    print(f"Loaded {len(file_list)} file paths from list")
            elif os.path.isdir(file_path):
                # It's a directory
                dir_files = get_all_files_paths_under(file_path)
                all_files.extend(dir_files)
                print(f"Found {len(dir_files)} files in directory: {file_path}")
            else:
                print(f"Warning: Path not found or invalid: {file_path}")
    
    if not all_files:
        print("Error: No input files found. Please provide valid file paths or directories")
        return
    
    print(f"Total files to process: {len(all_files)}")
    
    # Create output base directory if it doesn't exist
    os.makedirs(output_base_dir, exist_ok=True)

    # Open files with explicit UTF-8 encoding to support Hindi characters
    with codecs.open(processed_hashes_file_path, 'a+', encoding='utf-8') as processed_hashes_file, \
         codecs.open(skipped_files_log_path, 'a+', encoding='utf-8') as skipped_files_log:
        
        # Read existing hashes into memory
        print("Loading existing hashes...")
        processed_hashes_file.seek(0)  # Move to the beginning of the file
        existing_hashes = set()
        hash_count = 0
        
        for line in processed_hashes_file:
            hash_value = line.strip()
            if hash_value:  # Skip empty lines
                existing_hashes.add(hash_value)
                hash_count += 1
                if hash_count % 100000 == 0:
                    print(f"Loaded {hash_count} existing hashes...")

        print(f"Loaded {hash_count} existing hashes into memory")

        t0 = time.time()
        total_processed = 0
        total_duplicates = 0
        total_files_processed = 0

        # Process all files
        for input_file in all_files:
            try:
                total_files_processed += 1
                print(f"Processing file {total_files_processed}/{len(all_files)}: {input_file}")
                
                processed_count, duplicate_count = process_file(
                    input_file, 
                    output_base_dir, 
                    processed_hashes_file, 
                    existing_hashes,
                    args.output_batch_size,
                    args.hash_batch_size,
                    args.hash_algorithm,
                    args.flat_structure
                )

                # Update total counts
                total_processed += processed_count + duplicate_count
                total_duplicates += duplicate_count

                # Print progress
                print(f"File {total_files_processed} completed:")
                print(f"  - Unique records in this file: {processed_count}")
                print(f"  - Duplicates in this file: {duplicate_count}")
                print(f"  - Total records processed so far: {total_processed}")
                print(f"  - Total duplicates found so far: {total_duplicates}")
                print(f"  - Total unique records in dataset: {len(existing_hashes)}")
                print("-" * 50)
                
            except Exception as e:
                # Log skipped file with error message
                error_msg = f"Skipped file {input_file} due to error: {e}\n"
                skipped_files_log.write(error_msg)
                skipped_files_log.flush()
                print(f"Error processing file {input_file}: {e}. Skipping this file.")

        print(f"\n{'='*60}")
        print(f"DEDUPLICATION COMPLETED")
        print(f"{'='*60}")
        print(f"Total files processed: {total_files_processed}")
        print(f"Total processing time: {time.time() - t0:.2f} seconds")
        print(f"Total records processed: {total_processed}")
        print(f"Total duplicates found: {total_duplicates}")
        print(f"Total unique records: {len(existing_hashes)}")
        print(f"Output directory: {output_base_dir}")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Deduplicate JSONL files based on text content while preserving directory structure",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '--file-list', 
        nargs='+', 
        required=True,
        help="Input file paths, directories, or text files containing file paths to deduplicate"
    )
    
    parser.add_argument(
        '--output-dir', 
        required=True,
        help="Output directory where deduplicated files will be saved"
    )
    
    parser.add_argument(
        '--hash-file', 
        required=True,
        help="File to store/load processed hashes for deduplication"
    )
    
    parser.add_argument(
        '--log-file', 
        required=True,
        help="Log file for skipped files and errors"
    )
    
    parser.add_argument(
        '--output-batch-size', 
        type=int, 
        default=10000,
        help="Batch size for output file writes"
    )
    
    parser.add_argument(
        '--hash-batch-size', 
        type=int, 
        default=5000,
        help="Batch size for hash file writes"
    )
    
    parser.add_argument(
        '--hash-algorithm', 
        default='md5',
        choices=['md5', 'sha1', 'sha256'],
        help="Hash algorithm to use for deduplication"
    )
    
    parser.add_argument(
        '--flat-structure',
        action='store_true',
        help="Use flat directory structure for output (all files in output root)"
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(args)

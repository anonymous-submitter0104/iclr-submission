import argparse
import os
import shutil
from typing import Any
import time
import json
import argparse
# import cudf

from modifiers import HTMLTagModifier, QuotationUnifier, ExcessWhiteSpaceRemover

from nemo_curator import ScoreFilter, Sequential, AddId, FuzzyDuplicatesConfig, TaskDecontamination
from nemo_curator.datasets import DocumentDataset
from nemo_curator.filters import (
    RepeatingTopNGramsFilter,
    WordCountFilter, 
    SymbolsToWordsFilter,
    NumbersFilter,
    UrlsFilter,
    WhiteSpaceFilter,
    RepeatingDuplicateNGramsFilter,
    RepeatedParagraphsFilter,
    NonAlphaNumericFilter,
    ParenthesesFilter,
    RepeatedLinesFilter,
    MeanWordLengthFilter
)
from nemo_curator.modifiers.pii_modifier import PiiModifier
from nemo_curator.modifiers.unicode_reformatter import UnicodeReformatter
from nemo_curator.modifiers import BoilerPlateStringModifier
from nemo_curator.modules import ExactDuplicates
from nemo_curator.modules.modify import Modify
from nemo_curator.utils.distributed_utils import get_client
from nemo_curator.utils.file_utils import get_all_files_paths_under
from dask.distributed import Client, LocalCluster
from nemo_curator.classifiers import QualityClassifier

from nemo_curator.tasks import (
    ANLI, CB, PIQA, RTE, WSC, ArcChallenge, ArcEasy,
    BoolQ, Copa, Drop, MultiRC, OpenBookQA, Quac,
    Race, Record, Squad, TriviaQA, WebQA, WiC, Winogrande,
)
# os.environ['DASK_DATAFRAME__QUERY_PLANNING'] = "True"
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3,4,5,6,7"

TEXT_FIELD = "prompt"

def pre_imports():
    import cudf


def clean_and_unify(dataset: DocumentDataset) -> DocumentDataset:
    start = time.time()
    cleaners = Sequential(
        [
            Modify(BoilerPlateStringModifier(), text_field=TEXT_FIELD),
            Modify(HTMLTagModifier(), text_field=TEXT_FIELD),
            Modify(UnicodeReformatter(), text_field=TEXT_FIELD),
            Modify(QuotationUnifier(), text_field=TEXT_FIELD),
            Modify(ExcessWhiteSpaceRemover(), text_field=TEXT_FIELD),

        ]
    )
    cleaned_dataset = cleaners(dataset)
    print(f"\nclean_and_unify completed. Removed {len(dataset.df)-len(cleaned_dataset.df)} rows")
    print(f"Time taken {time.time()-start}s")
    return cleaned_dataset

def heuristic_filter(dataset: DocumentDataset) -> DocumentDataset:
    start = time.time()

    # Add a filter to remove empty documents first
    empty_doc_filter = ScoreFilter(
        WordCountFilter(min_words=1), 
        text_field=TEXT_FIELD, 
        score_field="word_count", 
        score_type=int
    )
    
    # Apply the empty document filter first
    filtered_dataset = empty_doc_filter(dataset)
    print(f"Removed {len(dataset.df)-len(filtered_dataset.df)} empty documents")
    filters = Sequential(
        [
            # ScoreFilter(WordCountFilter(min_words=50, max_words=500000),text_field=TEXT_FIELD,score_field="word_count",score_type=int),
            ScoreFilter(RepeatingTopNGramsFilter(n=2, max_repeating_ngram_ratio=0.2), text_field=TEXT_FIELD, score_type=float),
            ScoreFilter(RepeatingTopNGramsFilter(n=3, max_repeating_ngram_ratio=0.18), text_field=TEXT_FIELD, score_type=float),
            ScoreFilter(SymbolsToWordsFilter(max_symbol_to_word_ratio=0.12), text_field=TEXT_FIELD, score_type=float),
            ScoreFilter(NumbersFilter(max_number_to_text_ratio=0.2), text_field=TEXT_FIELD, score_type=float),
            ScoreFilter(UrlsFilter(max_url_to_text_ratio=0.15), text_field=TEXT_FIELD, score_type=float),
            ScoreFilter(WhiteSpaceFilter(max_white_space_ratio=0.2), text_field=TEXT_FIELD, score_type=float),
            ScoreFilter(NonAlphaNumericFilter(max_non_alpha_numeric_to_text_ratio=0.25), text_field=TEXT_FIELD, score_type=float),
        ]
    )
    filtered_dataset = filters(dataset)
    print(f"\nheuristic_filter completed. Removed {len(dataset.df)-len(filtered_dataset.df)} rows")
    print(f"Time taken {time.time()-start}s")
    return filtered_dataset

def dedupe(dataset: DocumentDataset) -> DocumentDataset:
    start = time.time()

    ######################## Exact dedup ########################
    add_id = AddId(id_field='id',id_prefix='mix_data',start_index=0)
    dataset = add_id(dataset)
    
    #deduplicator = ExactDuplicates(id_field="id", text_field="raw_content", hash_method="md5")
    deduplicator = ExactDuplicates(id_field="id", text_field=TEXT_FIELD, hash_method="md5")

    duplicates = deduplicator(dataset)
    docs_to_remove = duplicates.df.map_partitions(
        lambda x: x[x._hashes.duplicated(keep="first")]
    )

    duplicate_ids = list(docs_to_remove.compute().id)
    dataset_df = dataset.df
    deduped = dataset_df[~dataset_df.id.isin(duplicate_ids)]

    deduped_dataset = DocumentDataset(deduped)
    print(f"\ndedupe completed. Removed {len(dataset.df)-len(deduped_dataset.df)} rows")
    print(f"Time taken {time.time()-start}s")
    return deduped_dataset

def redact_pii(dataset: DocumentDataset) -> DocumentDataset:
    start = time.time()
    redactor = Modify(
        PiiModifier(
            supported_entities=["PHONE_NUMBER", "EMAIL_ADDRESS", "CREDIT_CARD"],
            anonymize_action="replace",
            device="gpu",
            batch_size=100
        ),
        text_field=TEXT_FIELD
    )
    redacted_dataset = redactor(dataset)
    # print(f"\nredact_pii completed. Removed {len(dataset.df)-len(redacted_dataset.df)} rows")
    print(f"Time taken {time.time()-start}s")
    return redacted_dataset

def process_chunk(file_path: str) -> None:
    """
    Run the curation pipeline on the TinyStories dataset.

    Args:
        args (Any): Command-line arguments.
        jsonl_dir (str): Directory path where the JSONL files are stored.
    """

    files = [file_path]
    print(f"Running curation pipeline on '{files}'...")

    print("Reading the data...")
    orig_dataset = DocumentDataset.read_json(files, add_filename=False)
    dataset = orig_dataset

    curation_steps = Sequential(
        [
            clean_and_unify,
            heuristic_filter,
            dedupe,
            redact_pii,
        ]
    )
    print("Executing the pipeline...")

    dataset = curation_steps(dataset)
    #cleardataset.df = dataset.df.drop(columns=['word_count', 'my_id'])
    #dataset.df = dataset.df[["raw_content", 'url', "date_download", "digest", "bucket", "cc_segment", "language", "language_score", "length", "nlines", "source_domain", "title"]]

    dataset = dataset.persist()

    print(f"Original dataset length: {len(orig_dataset.df)}")
    print(f"After dataprep: {len(dataset.df)}")
    print("Writing the results to disk...")

    out_path = "/workspace/Sunil/bharatgen/DATASET/nodes/instruction_dataset_step3/output/out_text.jsonl"
    # os.makedirs(out_path, exist_ok=True)
    # dataset.df = dataset.df.compute()
    dataset.to_json(out_path, write_to_filename=False)

def main(file_path):
    print("CPU Curation Pipeline Initiated.....")
    print("Retrieving Client......")
    client = get_client(cluster_type = 'gpu')
    client.run(pre_imports)
    print("Client Established......")
    print("Processing Chunks........")
    process_chunk(file_path)

    client.close()

if __name__ == "__main__":
    file_path = "/workspace/Sunil/bharatgen/DATASET/nodes/instruction_dataset_step3/text.jsonl"
    start = time.time()
    main(file_path)
    end = time.time()
    print(f"Time taken: {end - start}s")
    # import sys; sys.exit(1)

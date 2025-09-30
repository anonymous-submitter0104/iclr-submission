import os
import time
import orjson
import mmap
import ahocorasick
import argparse
import logging
import re
from dataclasses import dataclass
from typing import Set, Dict, List, Optional, Tuple
from pathlib import Path
from multiprocessing import Pool, cpu_count
from contextlib import contextmanager

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('toxic_filter_nemo_med.log')
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ProcessingResult:
    """Data class to store file processing results"""
    file: str
    total_lines: int
    filtered_lines: int
    removed_lines: int
    processing_time: float
    toxic_word_counts: Dict[str, int]

class ToxicFilter:
    # Word boundary characters that can appear before or after a word
    WORD_BOUNDARIES = {" ", "\t", "\n", "\r", ".", ",", "!", "?", ":", ";", 
                      "(", ")", "[", "]", "{", "}", '"', "'", "`", "-", "_",
                      "/", "\\", "|", "@", "#", "$", "%", "^", "&", "*", "+",
                      "=", "<", ">", "~"}

    def __init__(self, toxic_words_path: Path):
        """Initialize the ToxicFilter with a path to toxic words file"""
        self.toxic_words = self._load_toxic_words(toxic_words_path)
        self.toxic_trie = self._build_trie()
        # Build regex pattern for verification
        pattern = r'(?:^|[^\w]){0}(?:$|[^\w])'.format
        self.toxic_patterns = {
            word: re.compile(pattern(re.escape(word)), re.IGNORECASE)
            for word in self.toxic_words
        }
        logger.info(f"Initialized ToxicFilter with {len(self.toxic_words)} toxic words")

    def _load_toxic_words(self, file_path: Path) -> Set[str]:
        """Load toxic words from file with error handling"""
        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                return {line.strip().lower() for line in f if line.strip()}
        except Exception as e:
            logger.error(f"Error loading toxic words from {file_path}: {e}")
            raise

    def _build_trie(self) -> ahocorasick.Automaton:
        """Build an Aho-Corasick automaton for efficient first-pass matching"""
        trie = ahocorasick.Automaton()
        
        for word in self.toxic_words:
            # Only add the word itself - we'll verify boundaries later
            trie.add_word(word, word)
            
        trie.make_automaton()
        return trie

    def _verify_word_match(self, text: str, word: str) -> bool:
        """
        Verify that a word is actually a standalone word using regex.
        This is slower but more accurate than Aho-Corasick alone.
        """
        return bool(self.toxic_patterns[word].search(text))

    def find_toxic_word(self, text: str) -> Optional[str]:
        """
        Two-stage matching:
        1. Fast Aho-Corasick to find potential matches
        2. Regex verification to confirm exact word boundaries
        """
        try:
            # First pass: Get all potential matches using fast Aho-Corasick
            text_lower = text.lower()
            potential_matches = set(match[1] for match in self.toxic_trie.iter(text_lower))
            
            if not potential_matches:
                return None
            
            # Second pass: Verify matches have proper word boundaries
            # Add spaces at start and end to simplify boundary checking
            padded_text = f" {text} "
            
            # Check each potential match with regex
            for word in potential_matches:
                if self._verify_word_match(padded_text, word):
                    return word
                    
            return None
            
        except Exception as e:
            logger.warning(f"Error checking for toxic words: {e}")
            return None

@contextmanager
def open_files(input_path: Path, output_paths: Dict[str, Path]):
    """Context manager for handling multiple file operations"""
    files = {}
    try:
        files['input'] = open(input_path, "r", encoding="utf-8")
        files['mmap'] = mmap.mmap(files['input'].fileno(), 0, access=mmap.ACCESS_READ)
        
        for key, path in output_paths.items():
            files[key] = open(path, "w", encoding="utf-8")
        
        yield files
    
    finally:
        for f in files.values():
            try:
                f.close()
            except Exception as e:
                logger.error(f"Error closing file: {e}")

def process_file(input_path: str, output_base_dir: str, filter_obj: ToxicFilter) -> ProcessingResult:
    """Process a single file for toxic content"""
    start_time = time.time()
    stats = {
        'total_lines': 0,
        'filtered_lines': 0,
        'removed_lines': 0,
        'toxic_word_counts': {}
    }

    input_path = Path(input_path)
    output_paths = {
        'clean': Path(output_base_dir) / "filtered_files" / input_path.name,
        'toxic': Path(output_base_dir) / "toxic_files" / input_path.name,
        'error': Path(output_base_dir) / "error_files" / input_path.name
    }

    # Ensure output directories exist
    for path in output_paths.values():
        path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open_files(input_path, output_paths) as files:
            for line in iter(files['mmap'].readline, b""):
                stats['total_lines'] += 1
                
                try:
                    data = orjson.loads(line)
                    text = data.get("text", "")
                    
                    if not text:
                        files['clean'].write(line.decode("utf-8"))
                        stats['filtered_lines'] += 1
                        continue

                    toxic_word = filter_obj.find_toxic_word(text)
                    
                    if toxic_word:
                        data["toxic_word"] = toxic_word
                        files['toxic'].write(orjson.dumps(data).decode("utf-8") + "\n")
                        stats['removed_lines'] += 1
                        stats['toxic_word_counts'][toxic_word] = stats['toxic_word_counts'].get(toxic_word, 0) + 1
                    else:
                        files['clean'].write(line.decode("utf-8"))
                        stats['filtered_lines'] += 1
                        
                except orjson.JSONDecodeError as e:
                    logger.warning(f"JSON decode error in {input_path}: {e}")
                    files['error'].write(line.decode("utf-8"))
                except Exception as e:
                    logger.error(f"Unexpected error processing line in {input_path}: {e}")
                    files['error'].write(line.decode("utf-8"))

    except Exception as e:
        logger.error(f"Error processing file {input_path}: {e}")
        raise

    processing_time = time.time() - start_time
    logger.info(f"Processed {input_path} in {processing_time:.2f} seconds")

    return ProcessingResult(
        file=str(input_path),
        total_lines=stats['total_lines'],
        filtered_lines=stats['filtered_lines'],
        removed_lines=stats['removed_lines'],
        processing_time=processing_time,
        toxic_word_counts=stats['toxic_word_counts']
    )

def process_batch(file_list: List[str], toxic_words_path: str, output_base_dir: str) -> List[ProcessingResult]:
    """Process multiple files in parallel"""
    filter_obj = ToxicFilter(Path(toxic_words_path))
    num_processes = min(len(file_list), cpu_count())
    
    logger.info(f"Starting batch processing with {num_processes} processes")
    
    results = []
    with Pool(processes=num_processes) as pool:
        tasks = [
            pool.apply_async(
                process_file,
                (path, output_base_dir, filter_obj)
            )
            for path in file_list
        ]

        for task in tasks:
            try:
                results.append(task.get())
            except Exception as e:
                logger.error(f"Task failed: {e}")

    return results

def main():
    parser = argparse.ArgumentParser(description="Fast Toxic Word Filtering")
    parser.add_argument("--part", type=int, required=True, help="Part number to process")
    args = parser.parse_args()

    # Base Paths
    base_path = "/app"
    part = f"part_{args.part}"
    
    # File Paths
    file_paths = os.path.join(base_path, "toxic_final/toxic_paths_nemo_med", f"{part}.txt")
    toxic_words = os.path.join(base_path, "toxic_final/toxic_words.txt")
    output_base_dir = os.path.join(base_path, "toxic_final/results_nemo_med", part)

    os.makedirs(output_base_dir, exist_ok=True)

    logger.info(f"Starting processing for part {args.part}")
    
    try:
        # Read file paths
        with open(file_paths, "r", encoding="utf-8") as f:
            paths = [line.strip() for line in f if line.strip()]

        results = process_batch(paths, toxic_words, output_base_dir)
        
        # Log summary statistics
        total_processed = sum(r.total_lines for r in results)
        total_filtered = sum(r.filtered_lines for r in results)
        total_removed = sum(r.removed_lines for r in results)
        total_time = sum(r.processing_time for r in results)
        
        logger.info(f"""
Processing Summary:
-----------------
Total files processed: {len(results)}
Total lines processed: {total_processed:,}
Clean lines: {total_filtered:,}
Toxic lines: {total_removed:,}
Total processing time: {total_time:.2f} seconds
        """)
        
        print("\n🎉 All files processed successfully!")
        
    except Exception as e:
        logger.error(f"Fatal error in main process: {e}")
        raise

if __name__ == "__main__":
    main()

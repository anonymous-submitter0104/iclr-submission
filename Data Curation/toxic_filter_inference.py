import os
import json

def get_directory_size_gb(directory):
    """Returns the size of a directory in GB."""
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size / (1024 ** 3)  # Convert bytes to GB

# List of input directories
input_dirs = [
# paths here
]  # Add more directories as needed

# Define output directories
match_base_dir = "matches"
non_match_dir = "non_matches"

# Ensure output directories exist
os.makedirs(match_base_dir, exist_ok=True)
os.makedirs(non_match_dir, exist_ok=True)

# Load toxic words from file
toxic_word_file = "toxic_2.txt"

if not os.path.exists(toxic_word_file):
    raise FileNotFoundError(f"Toxic words file '{toxic_word_file}' not found.")

with open(toxic_word_file, "r", encoding="utf-8") as f:
    toxic_words = {line.strip().lower() for line in f if line.strip()}  # Convert to lowercase and remove blanks

print(f"✅ Loaded {len(toxic_words)} toxic words from '{toxic_word_file}'")

# Processing starts
total_files = 0
total_matches = 0
total_non_matches = 0

for input_dir in input_dirs:
    if not os.path.exists(input_dir):
        print(f"⚠️ Warning: Directory {input_dir} does not exist. Skipping.")
        continue

    print(f"\n📂 Processing directory: {input_dir}")

    for filename in os.listdir(input_dir):
        if filename.endswith(".jsonl"):
            total_files += 1
            input_path = os.path.join(input_dir, filename)
            non_match_path = os.path.join(non_match_dir, filename)

            print(f"  🔍 Processing file: {filename}")

            match_count = 0
            non_match_count = 0
            invalid_count = 0

            # Dictionary to store file handles for matched words
            match_file_handles = {}

            with open(input_path, "r", encoding="utf-8") as infile, \
                 open(non_match_path, "w", encoding="utf-8") as non_match_file:

                for line in infile:
                    try:
                        data = json.loads(line)
                        toxic_word = data.get("toxic_word", "").strip().lower()  # Normalize case
                        
                        if toxic_word in toxic_words:
                            # Create a subdirectory for the toxic word if not exists
                            toxic_word_dir = os.path.join(match_base_dir, toxic_word)
                            os.makedirs(toxic_word_dir, exist_ok=True)

                            # Open the corresponding toxic word file only once and store the handle
                            if toxic_word not in match_file_handles:
                                match_file_handles[toxic_word] = open(
                                    os.path.join(toxic_word_dir, filename),
                                    "a",
                                    encoding="utf-8"
                                )

                            # Write the matching JSON object to its respective toxic word file
                            match_file_handles[toxic_word].write(line)
                            match_count += 1
                        else:
                            non_match_file.write(line)
                            non_match_count += 1
                    except json.JSONDecodeError:
                        print(f"    ⚠️ Skipping invalid JSON in {filename}")
                        invalid_count += 1

            # Close all open file handles for matched toxic words
            for handle in match_file_handles.values():
                handle.close()

            total_matches += match_count
            total_non_matches += non_match_count

            # Get sizes of match and non-match directories
            match_size_gb = get_directory_size_gb(match_base_dir)
            non_match_size_gb = get_directory_size_gb(non_match_dir)

            print(f"    ✅ Matched: {match_count}, ❌ Non-Matched: {non_match_count}, ⚠️ Invalid: {invalid_count}")
            print(f"    📁 Size of 'matches/' directory: {match_size_gb:.3f} GB")
            print(f"    📁 Size of 'non_matches/' directory: {non_match_size_gb:.3f} GB")

# Final Summary
print("\n🎯 Processing complete!")
print(f"📄 Total files processed: {total_files}")
print(f"✅ Total matched entries: {total_matches}")
print(f"❌ Total non-matched entries: {total_non_matches}")
print(f"📁 Final size of 'matches/' directory: {get_directory_size_gb(match_base_dir):.3f} GB")
print(f"📁 Final size of 'non_matches/' directory: {get_directory_size_gb(non_match_dir):.3f} GB")

import os
import csv

def create_word_pairs_final(raw_file, splitted_file, output_csv):
    """
    Reads raw and splitted text files, pairs the words based on sandhi rules,
    and writes the pairs to a CSV file.

    This version correctly handles overlapping sandhis (e.g., for visarga and anusvara).
    """
    try:
        with open(raw_file, 'r', encoding='utf-8') as f_raw, \
             open(splitted_file, 'r', encoding='utf-8') as f_splitted, \
             open(output_csv, 'w', newline='', encoding='utf-8') as f_out:

            writer = csv.writer(f_out)
            writer.writerow(['combined word', 'splitted word'])

            raw_lines = f_raw.readlines()
            splitted_lines = f_splitted.readlines()

            for raw_line, splitted_line in zip(raw_lines, splitted_lines):
                raw_words = raw_line.strip().split()
                splitted_words = splitted_line.strip().split()

                i = 0
                while i < len(splitted_words):
                    raw_word = raw_words[i]
                    splitted_word = splitted_words[i]

                    # Case 1: Handle forward-linking sandhi (ends with '+')
                    if splitted_word.endswith('+') and (i + 1) < len(raw_words):
                        combined_word = f"{raw_word} {raw_words[i+1]}"
                        splitted_word_pair = f"{splitted_word}{splitted_words[i+1]}"
                        writer.writerow([combined_word, splitted_word_pair])

                    # Case 2: Handle self-contained sandhi ('+' is not at the end)
                    elif '+' in splitted_word and not splitted_word.endswith('+'):
                        writer.writerow([raw_word, splitted_word])
                    
                    # Always advance by one to check for overlaps
                    i += 1
    except FileNotFoundError as e:
        print(f"  Error: Could not find a required file. Skipping. Details: {e}")
    except Exception as e:
        print(f"  An unexpected error occurred: {e}")


def process_dataset(root_folder):
    """
    Walks through a root folder and processes any subdirectories that
    contain both 'raw.txt' and 'splitted.txt'.
    """
    print(f"Starting to process directories inside '{root_folder}'...")

    # os.walk is perfect for this, as it goes through the directory tree
    for dirpath, _, filenames in os.walk(root_folder):
        if 'raw.txt' in filenames and 'splitted.txt' in filenames:
            
            # Construct the full file paths
            raw_file_path = os.path.join(dirpath, 'raw.txt')
            splitted_file_path = os.path.join(dirpath, 'splitted.txt')
            output_csv_path = os.path.join(dirpath, 'sandhi-splitted.csv')

            print(f"\nFound required files in: '{dirpath}'")
            print("  -> Processing...")
            
            # Call the processing function on the found files
            create_word_pairs_final(raw_file_path, splitted_file_path, output_csv_path)
            
            print(f"  -> Successfully created '{output_csv_path}'")

    print("\nBatch processing complete.")


if __name__ == "__main__":
    # The name of the main folder containing your datasets
    dataset_directory = 'dataset'
    if not os.path.isdir(dataset_directory):
        print(f"Error: The directory '{dataset_directory}' was not found.")
        print("Please make sure the script is in the same parent folder as your 'dataset' directory.")
    else:
        process_dataset(dataset_directory)
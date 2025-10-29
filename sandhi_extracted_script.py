import os
import csv

def convert_to_csv(input_file_path, output_file_path):
    """
    Converts a tab-separated text file to a CSV file.

    Args:
        input_file_path (str): The full path to the input text file.
        output_file_path (str): The full path for the output CSV file.
    """
    try:
        with open(input_file_path, 'r', encoding='utf-8') as infile, \
             open(output_file_path, 'w', encoding='utf-8', newline='') as outfile:
            
            csv_writer = csv.writer(outfile)
            
            # Write the header row
            csv_writer.writerow(["Word", "Split"])
            
            # Process each line from the input file
            for line in infile:
                # Strip leading/trailing whitespace and split by the specific delimiter
                parts = line.strip().split('\t=>\t')
                
                # Write to CSV only if the line splits into exactly two parts
                if len(parts) == 2:
                    csv_writer.writerow(parts)
            
        print(f"✅ Successfully converted: {output_file_path}")

    except Exception as e:
        print(f"❌ An error occurred with {input_file_path}: {e}")

def process_dataset_folder(root_folder):
    """
    Walks through a root folder, finds 'sandhi-extracted.txt' files,
    and converts them to CSV.

    Args:
        root_folder (str): The path to the main dataset folder.
    """
    # Check if the root folder exists
    if not os.path.isdir(root_folder):
        print(f"❌ Error: The directory '{root_folder}' was not found.")
        return

    print(f"🚀 Starting conversion process in '{root_folder}'...")
    
    # os.walk traverses the directory tree top-down
    for dirpath, _, filenames in os.walk(root_folder):
        # Check if our target file is in the current directory
        if 'sandhi-extracted.txt' in filenames:
            
            # Construct the full path for the input .txt file
            txt_file_path = os.path.join(dirpath, 'sandhi-extracted.txt')
            
            # Construct the full path for the output .csv file
            csv_file_path = os.path.join(dirpath, 'sandhi-extracted.csv')
            
            # Call the conversion function
            convert_to_csv(txt_file_path, csv_file_path)
            
    print("✨ All done!")

# --- Main Execution ---
if __name__ == "__main__":
    # Set the path to your main dataset folder
    dataset_directory = "dataset"
    
    # Run the main processing function
    process_dataset_folder(dataset_directory)
import os
import shutil
import numpy as np

def merge_datasets():
    # Letters that we want to keep from the recently collected data
    keep_letters = {'C', 'G', 'K', 'M', 'N', 'R', 'S'}
    
    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # First, remove all files from data directory except the letters we want to keep
    existing_files = os.listdir('data')
    for file in existing_files:
        letter = file[0]  # Get the first character of filename
        if letter not in keep_letters:
            os.remove(os.path.join('data', file))
    
    # Copy files from demo_dataset for all other letters
    all_letters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    letters_to_copy = all_letters - keep_letters
    
    total_files_copied = 0
    
    for letter in letters_to_copy:
        source_dir = os.path.join('demo_dataset', letter)
        if os.path.exists(source_dir):
            files = os.listdir(source_dir)
            for i, file in enumerate(files):
                if file.endswith('.npy'):
                    source_path = os.path.join(source_dir, file)
                    dest_path = os.path.join('data', f'{letter}_{i}.npy')
                    try:
                        shutil.copy2(source_path, dest_path)
                        total_files_copied += 1
                    except Exception as e:
                        print(f"Error copying {file}: {e}")
    
    # Count files for each letter
    letter_counts = {}
    for file in os.listdir('data'):
        letter = file[0]
        letter_counts[letter] = letter_counts.get(letter, 0) + 1
    
    # Print summary
    print("\nDataset Summary:")
    print("-" * 40)
    print("Letter | Count")
    print("-" * 40)
    for letter in sorted(letter_counts.keys()):
        print(f"   {letter}   |  {letter_counts[letter]}")
    print("-" * 40)
    print(f"Total files copied from demo_dataset: {total_files_copied}")
    print(f"Total files in merged dataset: {sum(letter_counts.values())}")

if __name__ == "__main__":
    merge_datasets() 
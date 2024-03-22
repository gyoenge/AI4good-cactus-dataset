import shutil
import os

def move_files(source_folder, destination_folder):
    # Iterate over the root directory and its subdirectories
    for root, dirs, files in os.walk(source_folder):
        for filename in files:
            # Build the full file paths
            source_file = os.path.join(root, filename)
            destination_file = os.path.join(destination_folder, filename)
            
            # Check if it's a file (not a directory)
            if os.path.isfile(source_file):
                # Check if the file already exists in the destination folder
                if os.path.exists(destination_file):
                    # If file exists, generate a new name
                    name, extension = os.path.splitext(filename)
                    new_filename = name + "_1" + extension
                    i = 2
                    # Keep incrementing the number until we find a unique name
                    while os.path.exists(os.path.join(destination_folder, new_filename)):
                        new_filename = f"{name}_{i}{extension}"
                        i += 1
                    destination_file = os.path.join(destination_folder, new_filename)
                
                # Move the file to the destination folder
                shutil.move(source_file, destination_file)

# Example usage:
source_folder = 'C:/Users/User/Downloads/1'
destination_folder = 'C:/Users/User/Downloads/slide_dataset'

move_files(source_folder, destination_folder)

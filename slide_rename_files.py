import os

def rename_files(folder_path):
    # Get the list of files in the folder
    files = os.listdir(folder_path)

    # Initialize a counter for numbering the files
    count = 1

    # Iterate through each file in the folder
    for filename in files:
        # Check if the filename matches the pattern 'slide-*.jpg'
        if filename.startswith('slide-') and filename.endswith('.jpg'):
            # Construct the new filename
            new_filename = f'slide_{count}.jpg'

            # Build the full file paths
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)

            # Rename the file
            os.rename(old_file_path, new_file_path)

            # Increment the counter for the next file
            count += 1

# Example usage:
folder_path = 'C:/Users/User/Downloads/slide_dataset'
rename_files(folder_path)
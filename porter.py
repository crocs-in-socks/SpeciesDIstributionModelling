folder_path = r'D:\Projects\Project-1\CHELSA-clt'
file_name = r'D:\Projects\Project-1\Code\envidatS3paths.txt'

import os
import requests
from tqdm import tqdm
import time
import sys

# Make sure the directory exists
os.makedirs(folder_path, exist_ok=True)

# Function to download a file with a timeout check
def download_file(url, folder, max_time=20):
    local_filename = os.path.join(folder, os.path.basename(url))
    
    # Start timing the download
    start_time = time.time()
    
    try:
        # Make a GET request to download the file
        with requests.get(url, stream=True) as response:
            # Get the total file size from headers
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kilobyte
            
            # Use tqdm to show download progress
            with tqdm(total=total_size, unit='iB', unit_scale=True, desc=os.path.basename(url)) as progress_bar:
                with open(local_filename, 'wb') as file:
                    for data in response.iter_content(block_size):
                        progress_bar.update(len(data))  # Update progress bar
                        file.write(data)  # Write data to the file

                        # Check if the total elapsed time exceeds max_time
                        elapsed_time = time.time() - start_time
                        if elapsed_time > max_time:
                            print(f"Download of {url} exceeded {max_time} seconds.")
                            # restart_program()  # Restart the script if the time limit is exceeded
                            return False

        print(f"Downloaded {url}")
        return True  # Return True on success

    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False  # Return False on failure

# Function to restart the program
def restart_program():
    print("Restarting program...")
    python = sys.executable
    os.execv(python, [python] + sys.argv)  # Restart the program with the same arguments

# Function to remove a line from the file
def remove_url_from_file(url, file_name):
    # Read all the lines from the file
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Write back all lines except the one that matches the URL to be removed
    with open(file_name, 'w') as file:
        for line in lines:
            if line.strip() != url:
                file.write(line)

# Function to append the failed URL to the end of the file
def append_url_to_file(url, file_name):
    with open(file_name, 'a') as file:  # 'a' mode to append
        file.write(f"{url}\n")

# Read URLs from the text file
with open(file_name, 'r') as file:
    urls = [url.strip() for url in file.readlines()]  # Strip whitespace/newlines

# Download each file and restart if the download exceeds 20 seconds
for url in urls:
    if download_file(url, folder_path, max_time=20):  # Restart if a file takes more than 20 seconds to download
        remove_url_from_file(url, file_name)  # Remove the URL from the file after successful download
    else:
        # If download fails, move the URL to the end of the file
        print(f"Failed to download {url}. Moving it to the end of the file.")
        remove_url_from_file(url, file_name)  # Remove it from its current position
        append_url_to_file(url, file_name)  # Add it to the end of the file

print("Download complete!")

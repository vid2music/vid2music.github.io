#!/usr/bin/env python3

import os
import subprocess
import sys

def process_mp4_files(directory):
    """
    Recursively process all .mp4 files in the given directory,
    placing 'moov' atom at the front (faststart) and overwriting
    the original file in-place.
    """
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(".mp4"):
                full_path = os.path.join(root, filename)
                
                # Use a temp file with .temp.mp4 to ensure ffmpeg recognizes the container
                # e.g. original_file.mp4 => original_file.mp4.temp.mp4
                temp_file = f"{full_path}.temp.mp4"

                command = [
                    "ffmpeg",
                    "-y",               # Overwrite if temp_file already exists
                    "-i", full_path,
                    "-movflags", "faststart",
                    "-c", "copy",
                    temp_file
                ]

                print(f"Processing: {full_path}")
                try:
                    subprocess.run(command, check=True)
                    
                    # If ffmpeg succeeds, remove original and rename temp to original name
                    os.remove(full_path)
                    os.rename(temp_file, full_path)
                    print(f"Replaced with faststart version: {full_path}\n")

                except subprocess.CalledProcessError as e:
                    print(f"Error processing '{full_path}': {e}\n")
                    if os.path.exists(temp_file):
                        os.remove(temp_file)

if __name__ == "__main__":
    """
    Usage:
        python bulk_inplace_mp4_processing.py [directory_path]

    If no directory path is provided, the current directory is used.
    """
    if len(sys.argv) > 1:
        directory_to_process = sys.argv[1]
    else:
        directory_to_process = "."

    process_mp4_files(directory_to_process)

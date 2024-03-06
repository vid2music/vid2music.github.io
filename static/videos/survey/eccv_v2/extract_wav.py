import os
import subprocess

# Specify the directory containing the .mp4 files
source_dir = './'

# Loop through all files in the directory
for filename in os.listdir(source_dir):
    if filename.endswith(".mp4"):
        # Construct the full file path
        full_path = os.path.join(source_dir, filename)
        # Construct the output file name by replacing .mp4 with .wav
        output_file = os.path.join(source_dir, filename.replace(".mp4", ".wav"))
        
        # Construct the ffmpeg command
        cmd = ['ffmpeg', '-i', full_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', output_file]
        
        # Execute the command
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print("Conversion completed.")

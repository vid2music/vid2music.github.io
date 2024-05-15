import os
import subprocess

# Define the paths to the folders
folder_a = './nips_music/Ours'
folder_b = './nips_music/Video2Music'
output_folder = './nips_music/Video2Music_v2'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Function to replace audio using FFmpeg
def replace_audio(video_a_path, video_b_path, output_path):
    command = [
        'ffmpeg',
        '-i', video_a_path,     # Input video from folder A
        '-i', video_b_path,     # Input video from folder B (for audio)
        '-c:v', 'copy',         # Copy the video stream
        '-map', '0:v:0',        # Map video from the first input
        '-map', '1:a:0',        # Map audio from the second input
        output_path             # Output file path
    ]
    subprocess.run(command, check=True)

# Iterate over files in folder A
for filename in os.listdir(folder_a):
    if filename.endswith(('.mp4', '.mkv', '.avi', '.mov')):  # Add more video extensions if needed
        video_a_path = os.path.join(folder_a, filename)
        video_b_path = os.path.join(folder_b, filename)
        output_path = os.path.join(output_folder, filename)

        # Check if corresponding file exists in folder B
        if os.path.exists(video_b_path):
            replace_audio(video_a_path, video_b_path, output_path)
            print(f"Processed {filename}")
        else:
            print(f"Corresponding file for {filename} not found in folder B")

print("Audio replacement completed.")

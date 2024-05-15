import os
import subprocess

# Define the paths to the folders
folder_a = './nips_music/download_ori'
folder_b = './nips_music/CMT'
output_folder = './nips_music/CMT_v2'

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Function to replace audio and cut the video using FFmpeg
def replace_audio_and_cut(video_a_path, video_b_path, output_path, start_time=0, duration=10):
    command = [
        'ffmpeg',
        '-i', video_a_path,     # Input video from folder A
        '-i', video_b_path,     # Input video from folder B (for audio)
        '-ss', str(start_time), # Start time for cutting
        '-t', str(duration),    # Duration of the cut
        '-c:v', 'libx264',      # Use libx264 codec for video
        '-c:a', 'aac',          # Use aac codec for audio
        '-map', '0:v:0',        # Map video from the first input
        '-map', '1:a:0',        # Map audio from the second input
        '-y',                   # Overwrite output file if exists
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
            replace_audio_and_cut(video_a_path, video_b_path, output_path)
            print(f"Processed {filename}")
        else:
            print(f"Corresponding file for {filename} not found in folder B")

print("Audio replacement and cutting completed.")

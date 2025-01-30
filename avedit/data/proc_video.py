import os
import glob

# Base directory where folders are located
base_path = "./"

# Get all existing folders
folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]

for folder in folders:
    # Define new folder with "_new" suffix
    new_folder = os.path.join(base_path, f"{folder}_new")
    
    # Create the new folder if it doesn't exist
    os.makedirs(new_folder, exist_ok=True)
    print(f"Created folder: {new_folder}")

    # Find all MP4 files in the current folder
    video_files = glob.glob(os.path.join(base_path, folder, "*.mp4"))

    for video in video_files:
        # Extract filename
        filename = os.path.basename(video)
        
        # Define the new file path in the corresponding "_new" folder
        new_file_path = os.path.join(new_folder, filename)

        # FFmpeg command to ensure HTML compatibility
        cmd = f'ffmpeg -y -i "{video}" -c:v libx264 -preset slow -crf 23 -c:a aac -b:a 128k -movflags +faststart -pix_fmt yuv420p "{new_file_path}"'

        # Execute the command
        os.system(cmd)
        print(f"Processed: {filename} -> {new_file_path}")

print("All videos have been re-encoded and are now HTML-compatible!")

import os
import re
import subprocess
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# Define the list of video names
video_names = [
    "009_yidjX2NFcvw_0009",
    "017_jXOi-HRk9vA_0007",
    "022_50gitCL5wY4_0011",
    "023_1jt6ad6KmyA_0005",
    "034_R8TtpfYljkc_0008",
    "039_lfph10Q8wL8_0011",
    "054_gdMrinpq5kw_0010",
    "055_5_YC__FQnOA_0005",
    "058_FSbTBxcdmDo_0006",
    "058_j0Q_oAquGNo_0019",
    "060_gqUJP3i2eOU_0013",
    "070_2yUFH0uM9IM_0013",
    "071_KhTReROnT0A_0004",
    "072_MUpIfp8iTUE_0005",
    "075_nmYi5u9BhtI_0014",
    "878_2dyEnOo3yJ8_0033",
    "878_v5nB2OJnCko_0001",
    "004_h9Me4KIiPLU_0011",
    "016_F60bMyARUvk_0015",
    "022_KQAlMilSo3Q_0012"
]

# Regular expression pattern to extract YouTube ID and timestamps
pattern = re.compile(r'_(.*?)_(\d{4})')

for video_name in video_names:
    match = pattern.search(video_name)
    if match:
        yt_id = match.group(1)
        start_seconds = int(match.group(2)) * 10
        end_seconds = start_seconds + 10

        # Check if the video is available on YouTube
        check_command = [
            'yt-dlp',
            '-f', 'best',
            '--get-filename',
            f'https://www.youtube.com/watch?v={yt_id}'
        ]
        try:
            filename = subprocess.check_output(check_command, stderr=subprocess.STDOUT).decode().strip()
        except subprocess.CalledProcessError:
            print(f"Video {yt_id} is not available on YouTube. Skipping...")
            continue

        # Download the video using yt-dlp
        download_command = [
            'yt-dlp',
            '-f', 'best',
            '-o', f'{yt_id}.%(ext)s',
            f'https://www.youtube.com/watch?v={yt_id}'
        ]
        subprocess.run(download_command, check=True)

        # Find the downloaded video file
        video_file = None
        for file in os.listdir('.'):
            if file.startswith(yt_id):
                video_file = file
                break

        if video_file:
            # Clip the video
            clipped_file = f'clipped_{video_name}.mp4'
            ffmpeg_extract_subclip(video_file, start_seconds, end_seconds, targetname=clipped_file)

            # Optionally, delete the original downloaded file
            os.remove(video_file)

            print(f"Downloaded and clipped {video_name} to {clipped_file}")
        else:
            print(f"Failed to find the downloaded video for {yt_id}")
    else:
        print(f"Invalid video name format: {video_name}")

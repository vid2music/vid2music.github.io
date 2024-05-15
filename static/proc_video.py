import glob
import os

# Get all .mp4 file paths
all_path = glob.glob('./nips_music/*/*.mp4')

for tmp in all_path:
    # Create the target directory if it doesn't exist
    target_dir = os.path.dirname(tmp.replace('nips_music', 'tmp_video'))
    os.makedirs(target_dir, exist_ok=True)
    
    # Construct and run the ffmpeg command
    cmd = 'ffmpeg -y -i {} -vcodec libx264 -acodec aac -vf "scale=224:224" {}'.format(tmp, tmp.replace('nips_music', 'tmp_video'))
    os.system(cmd)

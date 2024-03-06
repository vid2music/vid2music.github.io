"""
Download the clips within the MusicCaps dataset from YouTube.

Requires:
	- ffmpeg
	- yt-dlp
	- datasets[audio]
	- torchaudio
"""
import subprocess
import os
from pathlib import Path

# from datasets import load_dataset, Audio
from ipdb import set_trace
import time

from tqdm.contrib.concurrent import thread_map

from multiprocessing.pool import ThreadPool

from tqdm import tqdm
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging 
import csv

logging.basicConfig(filename="std.log", 
					format='%(asctime)s %(message)s', 
					filemode='w') 

logger=logging.getLogger() 

def download_clip(
	video_identifier,
	output_filename,
	out_compress_path,
	num_attempts=5,
	url_base='https://www.youtube.com/watch?v='
):

	status = os.path.exists(output_filename)
	if status:
		return status, 'Downloaded'
	# status = False



	start_time = int(float(video_identifier[1]))
	end_time = start_time + 10
	video_identifier = video_identifier[0]
	
	# yt-dlp --quiet --no-warnings -S "height:480" -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b"  -o "{output_filename}" "{url_base}{video_identifier}"
	# command = f"""
	# 	yt-dlp --quiet --no-overwrites --no-warnings -S "height:240" -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b "  -o "{output_filename}" --download-sections "*{start_time}-{end_time}" "{url_base}{video_identifier}"
	# """.strip()

	# command = f"""
	# 	yt-dlp --quiet --no-overwrites --no-warnings -f "bestvideo[height<=240]+bestaudio/best[height<=240]" --recode-video mp4 --download-sections "*{start_time}-{end_time}" --force-keyframes-at-cuts -o "{output_filename}"  "{url_base}{video_identifier}"
	# """.strip()

	command = f"""
		yt-dlp --quiet --no-overwrites --no-warnings -S "vcodec:h264/acodec:m4a"  -f "bestvideo[height<=240]+bestaudio/best[height<=360]/best[height<=480]/best[height<=720]"  --recode-video mp4 --download-sections "*{start_time}-{end_time}" --force-keyframes-at-cuts  --postprocessor-args "-c:a aac -b:a 128k -ar 16000" -o "{output_filename}"  "{url_base}{video_identifier}"
	""".strip()


	# yt-dlp --quiet --no-overwrites --no-warnings -f "bestvideo[height<=240]+bestaudio/best[height<=240]" --recode-video mp4 --download-sections "*328-338" -o "./gg.mp4"  "https://www.youtube.com/watch?v=-7crpsqa6sc"

	attempts = 0
	while True:
		time.sleep(1)
		try:
			output = subprocess.check_output(command, shell=True,
												stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError as err:
			attempts += 1
			if attempts == num_attempts:
				return status, err.output
		else:
			break

	# Check if the video was successfully saved.
	status = os.path.exists(output_filename)
	# if status:
	#     cmd_downsample = f"""
	#         ffmpeg -i {output_filename} -vf "fps=24,scale=224:224" -c:a aac -map 0 {out_compress_path}
	#     """.strip()

	#     output = subprocess.check_output(cmd_downsample, shell=True, stderr=subprocess.STDOUT)
	
	# if os.path.exists(out_compress_path):
	#     os.remove(output_filename)

	if not status:
		print("Fail:", command) 
	return status, 'Downloaded'


def main(
	data_dir: str,
	sampling_rate: int = 44100,
	yt_list = None
):
	"""
	Download the clips within the MusicCaps dataset from YouTube.

	Args:
		data_dir: Directory to save the clips to.
		sampling_rate: Sampling rate of the audio clips.
		limit: Limit the number of examples to download.
		num_proc: Number of processes to use for downloading.
		writer_batch_size: Batch size for writing the dataset. This is per process.
	"""

	# ds = load_dataset('google/MusicCaps', split='train')
	# if limit is not None:
	#     print(f"Limiting to {limit} examples")
	#     ds = ds.select(range(limit))
	
	data_dir = Path(data_dir)
	data_dir.mkdir(exist_ok=True, parents=True)

	def process(yt_info):
		# yt_info = yt_full.split('watch?v=')[-1]

		outfile_path = str(data_dir / f"{yt_info[0]}.mp4")
		outfile_path2 = str(data_dir / f"{yt_info[0]}.mp4")
		status = True
		if not os.path.exists(outfile_path):
			status = False
			status, log = download_clip(
				yt_info,
				outfile_path,
				outfile_path2
			)
		return yt_info
	
	with tqdm(total=len(yt_list)) as pbar:
		with ThreadPoolExecutor(max_workers=64) as ex:
			futures = [ex.submit(process, url) for url in yt_list]
			for future in as_completed(futures):
				result = future.result()
				pbar.update(1)





if __name__ == '__main__':


	# id 14 == music

	prev = -1

	count_line = 0
	all_yt_name = []
	with open('./ncentroids-500-subset_size-10M.csv', newline='') as csvfile:
		csvreader = csv.reader(csvfile)
		for row in csvreader:
			all_yt_name.append(row)



	main(
		'/data/yanbo/download_tool/acav10m',
		sampling_rate=16000,
		yt_list = all_yt_name[:5000000]
		)


#####
###


# test alive:  yt-dlp -S "vcodec:h264/acodec:m4a"  -f "bestvideo[height<=240]+bestaudio/best[height<=360]/best[height<=480]/best[height<=720]"  --recode-video mp4 --download-sections "*10-20" --force-keyframes-at-cuts  --postprocessor-args "-c:a aac -b:a 128k -ar 16000" -o "gg.mp4"  "https://www.youtube.com/watch?v=-ZJqu_4zLMc"

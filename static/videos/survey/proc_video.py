import glob
from ipdb import set_trace

import os
import random
import copy


all_path = glob.glob('./tmp_v2/*.mp4')


for tmp in all_path:

    # cmd = 'ffmpeg -y -i {} -vcodec libx264 -acodec aac {}'.format(tmp,tmp.replace('tmp_v2','eccv_v2'))
    cmd = 'ffmpeg -y -i {} -vcodec libx264 -acodec aac -vf "scale=224:224" {}'.format(tmp, tmp.replace('tmp_v2', 'eccv_v2'))

    os.system(cmd)  

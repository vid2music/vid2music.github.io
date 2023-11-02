import glob
from ipdb import set_trace

import os
import random
import copy


all_path = glob.glob('./tmp/*.mp4')


for tmp in all_path:

    cmd = 'ffmpeg -y -i {} -vcodec libx264 -acodec aac {}'.format(tmp,tmp.replace('tmp','gg'))
    os.system(cmd)  

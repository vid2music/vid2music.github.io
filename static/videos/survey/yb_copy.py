import glob
from ipdb import set_trace

import os
import random
import copy


all_path = glob.glob('./*.mp4')

cadidate = ['avbeat', 'baseline', 'cmt','nce', 'VidCaption']
count = 0 
all_rand_order = []
numbers = list(range(5))
for tmp_path in all_path:
    random.shuffle(numbers)
    all_rand_order.append(copy.deepcopy(numbers))

    count +=1
    name = tmp_path.split('/')[-1]


    inst_count = 0
    for tmp_idx in numbers:
        print(tmp_idx)
        inst_count +=1
        source = '/mnt/c/Users/harry/Downloads/demo/demo500/{}/'.format(cadidate[tmp_idx])+name
        cmd = 'cp {} {}'.format(source, './tmp/{}-{}.mp4'.format(count,inst_count))
        os.system(cmd) 
        cmd = 'cp {} {}'.format(source, './tmp/{}-{}.wav'.format(count,inst_count))
        os.system(cmd)  
set_trace()
# !/usr/bin/python3.4

import os
import sys
from asr_run import *

root_dir = sys.argv[1]
video_dir = root_dir
sound_dir = '../sound/'
txt_dir = '../txt/'
log_dir = '../log/'


for parent, dirs, files in os.walk(root_dir):
	for file in files:
		filename = file[:-4]
		run(file, filename, video_dir, sound_dir, txt_dir, log_dir)
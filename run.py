# !/usr/bin/python3.4

import os
import sys
from asr_run import *
import time
import numpy as np
# import threading

machine_index = 0

root_dir = sys.argv[1]
video_dir = root_dir
sound_dir = '../sound/'
txt_dir = '../txt/'
log_dir = '../log/'
file_list = video_dir+'files.npy'

start_time = time.time()
count = 0
total_minute = 0
total_second = 0

file_list = np.load(file_list).tolist()
file_amount = len(file_list)

avg = int(file_amount/11)
if index != 10:
	files = file_list[index*avg:(index+1)*avg]
else:
	files = file_list[10*avg:]

for file in files:
	count += 1
	filename = file[:-4]
	duration = run(file, filename, video_dir, sound_dir, txt_dir, log_dir).split(':')[1].split(' ')
	if len(duration) == 3:
		if 'mn' in duration[1]:
			minute = int(duration[1][:-2])
			second = int(duration[2][:-1])
		elif 's' in duration[1]:
			minute = 0
			second = int(duration[1][:-1])
			ms = int(duration[2][:-2])
			second += ms/1000
	elif len(duration) == 2:
		if 'mn' in duration[1]:
			minute = int(duration[1][:-2])
			second = 0
		elif 's' in duration[1]:
			minute = 0
			second = int(duration[1][:-1])
		else:
			minute = second = 0
	else:
		minute = second = 0
	total_minute += minute
	total_second += second

# for parent, dirs, files in os.walk(root_dir):
# 	for file in files:
# 		count += 1
# 		filename = file[:-4]
# 		duration = run(file, filename, video_dir, sound_dir, txt_dir, log_dir).split(':')[1].split(' ')
# 		if len(duration) == 3:
# 			if 'mn' in duration[1]:
# 				minute = int(duration[1][:-2])
# 				second = int(duration[2][:-1])
# 			elif 's' in duration[1]:
# 				minute = 0
# 				second = int(duration[1][:-1])
# 				ms = int(duration[2][:-2])
# 				second += ms/1000
# 		elif len(duration) == 2:
# 			if 'mn' in duration[1]:
# 				minute = int(duration[1][:-2])
# 				second = 0
# 			elif 's' in duration[1]:
# 				minute = 0
# 				second = int(duration[1][:-1])
# 			else:
# 				minute = second = 0
# 		else:
# 			minute = second = 0
# 		total_minute += minute
# 		total_second += second

total_duration = total_minute + total_second/60.0

end_time = time.time()
f = open(log_dir+'REPORT-'+str(index)+'.log', 'w')
result = str(count) + ' Videos, Total Duration ' + str(total_duration) + ' minutes, Total Time Cost ' + str((end_time - start_time)/60.0) + ' minutes.'
f.write(str)
f.close()
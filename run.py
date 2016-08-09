# !/usr/bin/python3.4

import os
import sys
from asr_run import *
# import time
# import numpy as np

# import threading
# import threading

index = 0

# root_dir = sys.argv[1]
# video_dir = root_dir
# sound_dir = '../sound/'
# sound_dir = '../training-1/'
sound_dir = '/home/orcuslc/MED/training-1/sound/'
txt_dir = '/home/orcuslc/MED/training-1/txt/'
log_dir = '/home/orcuslc/MED/training-1/log/'
# file_list = sound_dir+'files.npy'

start_time = time.time()
count = 0
total_minute = 0
total_second = 0

file = sys.argv[1]
filename = file[-13:-4]
asr_run(file, filename, txt_dir, log_dir, start_time)

# listlock = threading.RLock()

# file_amount = 1
# while file_amount >= 1:
# 	time.sleep(np.random.random())
# 	count += 1
# 	# listlock.acquire()
# 	files = np.load(file_list).tolist()
# 	file_amount = len(files)
# 	file = files.pop(0)
# 	np.save(file_list, files)
# 	filename = file[:-4]
# 	file = sound_dir + file
# 	print(file+' Started!')
# 	asr_run(sound_dir+file, filename, txt_dir, log_dir)

# avg = int(file_amount/11)
# if index != 10:
# 	files = file_list[index*avg:(index+1)*avg]
# else:
# 	files = file_list[10*avg:]

# for file in files:
# 	count += 1
# 	filename = file[:-4]
# 	duration = run(file, filename, video_dir, sound_dir, txt_dir, log_dir).split(':')[1].split(' ')
# 	if len(duration) == 3:
# 		if 'mn' in duration[1]:
# 			minute = int(duration[1][:-2])
# 			second = int(duration[2][:-1])
# 		elif 's' in duration[1]:
# 			minute = 0
# 			second = int(duration[1][:-1])
# 			ms = int(duration[2][:-2])
# 			second += ms/1000
# 	elif len(duration) == 2:
# 		if 'mn' in duration[1]:
# 			minute = int(duration[1][:-2])
# 			second = 0
# 		elif 's' in duration[1]:
# 			minute = 0
# 			second = int(duration[1][:-1])
# 		else:
# 			minute = second = 0
# 	else:
# 		minute = second = 0
# 	total_minute += minute
# 	total_second += second

# for parent, dirs, files in os.walk(sound_dir):
# 	for file in files:
# 		if file[-4:] != '.wav':
# 			continue
# 		count += 1
# 		filename = file[:-4]
# 		print(file+' Started!')
# 		asr_run(sound_dir+file, filename, txt_dir, log_dir)
		# duration = run(file, filename, video_dir, sound_dir, txt_dir, log_dir).split(':')[1].split(' ')
		# if len(duration) == 3:
		# 	if 'mn' in duration[1]:
		# 		minute = int(duration[1][:-2])
		# 		second = int(duration[2][:-1])
		# 	elif 's' in duration[1]:
		# 		minute = 0
		# 		second = int(duration[1][:-1])
		# 		ms = int(duration[2][:-2])
		# 		second += ms/1000
		# elif len(duration) == 2:
		# 	if 'mn' in duration[1]:
		# 		minute = int(duration[1][:-2])
		# 		second = 0
		# 	elif 's' in duration[1]:
		# 		minute = 0
		# 		second = int(duration[1][:-1])
		# 	else:
		# 		minute = second = 0
		# else:
		# 	minute = second = 0
		# total_minute += minute
		# total_second += second

# total_duration = total_minute + total_second/60.0

# end_time = time.time()
# f = open(log_dir+'REPORT-'+str(index)+'.log', 'w')
# result = str(count)
# result = str(count) + ' Videos, Total Duration ' + str(total_duration) + ' minutes, Total Time Cost ' + str((end_time - start_time)/60.0) + ' minutes.'
# f.write(result)
# f.close()
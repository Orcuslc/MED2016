# Dump sound
import os, sys, subprocess, re, time
# from filt import *
# from change_freq import change_frequency

index = 0
framerate = 8000
sound_dir = '../sound/'
video_dir = '../'
log_dir = '../log/'


def get_info(video, video_name, video_dir):
	print(video_name + ' started!')
	cmd = 'mediainfo ' + video_dir + video + ' |grep Duration'
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	a = p.wait()
	(stdoutput, erroutput) = p.communicate()
	stdoutput = stdoutput.decode('utf-8').split('\n')[0]
	print(stdoutput)
	return stdoutput

def dump_wave(video, video_name, video_dir, sound_dir):
	cmd = 'mplayer ' + video_dir + video + ' -novideo -ao pcm:file="' + sound_dir + video_name + '.wav' + '" -srate ' + str(framerate)
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	a = p.wait()
	(stdoutput, erroutput) = p.communicate()
	print(video_name + ' dump succeeded!')
	# sound = sound_dir + video_name + '.wav'

if __name__ == '__main__':
	root_dir = sys.argv[1]

	start_time = time.time()
	count = 0
	total_minute = 0
	total_second = 0
	
	for parent, dirs, files in os.walk(root_dir):
		for file in files:
			count += 1
			filename = file[:-4]
			duration = get_info(file, filename, video_dir)
			dump_wave(file, filename, video_dir, sound_dir)
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

total_duration = total_minute + total_second/60.0
end_time = time.time()
f = open(log_dir+'DUMP_REPORT-'+str(index)+'.log', 'w')
result = str(count) + ' Videos, Total Duration ' + str(total_duration) + ' minutes, Total DUMP Time Cost ' + str((end_time - start_time)/60.0) + ' minutes.'
f.write(result)
f.close()
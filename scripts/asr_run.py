import os
import sys
import subprocess
from change_freq import change_frequency
from filt import *
import re
import time

framerate = 8000
kaldi_dir = '/home/orcuslc/MED/kaldi'
nnet = '/home/orcuslc/MED/nnet_a_gpu_online'
graph = '/home/orcuslc/MED/graph'
online2bin = 'online2-wav-nnet2-latgen-threaded'


def timeit(func):
	def wrapper(*args, **kw):
		time1 = time.time()
		result = func(*args, **kw)
		time2 = time.time()
		print('Total time:', str(time2-time1), 's\n')
		return result
	return wrapper

def get_info(video, video_name, video_dir):
	print(video_name + ' started!')
	cmd = 'mediainfo ' + video_dir + video + ' |grep Duration'
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	a = p.wait()
	(stdoutput, erroutput) = p.communicate()
	stdoutput = stdoutput.decode('utf-8').split('\n')[0]
	print(stdoutput)
	return stdoutput

def dump_wav(video, video_name, video_dir, sound_dir):
	cmd = 'mplayer ' + video_dir + video + ' -novideo -ao pcm:file="' + sound_dir + video_name + '.wav' + '" -srate ' + str(framerate)
	# print(cmd)
	p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	a = p.wait()
	(stdoutput, erroutput) = p.communicate()
	print(video_name + ' dump succeeded!')
	sound = sound_dir + video_name + '.wav'
	sound_filter(sound, [300, 1000], [200, 2000], set_eq)
	print(video_name + ' filting succeeded!')
	return sound

# def handle_sound(sound, sound_name, tmp_dir):
# 	sound_filter(sound, [300, 1000], [200, 2000], set_eq)

def asr_run(sound, sound_name, txt_dir, log_dir, start_time):
	# change_frequency(sound, framerate)
	sound_filter(sound, [300, 1000], [200, 2000], set_eq)
	online_decode_dir = kaldi_dir + '/src/online2bin/' + online2bin
	param = 			' --do-endpointing=false' + \
			' --config=' + nnet + '/conf/online_nnet2_decoding.conf' + \
			' --max-active=7000 --beam=15.0 --lattice-beam=6.0 --acoustic-scale=0.1' + \
			' --word-symbol-table=' + graph + '/words.txt ' + \
			nnet + '/final.mdl ' + graph + '/HCLG.fst ' + \
			'"ark:echo utterance-id1 utterance-id1|"' + \
			' "scp:echo utterance-id1 ' + sound + '|" ' + \
			'ark:/dev/null'

	p = subprocess.Popen(online_decode_dir + param, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	a = p.wait()
	(stdoutput, erroutput) = p.communicate()

	stdoutput = stdoutput.decode('utf-8')
	# print(stdoutput)
	# try:
	res = re.findall(r'utterance-id1\s.+', stdoutput)[1][14:] + '\n'
	# except IndexError:
	# 	res = '\n'

	f = open(txt_dir+sound_name+'.txt', 'w')
	f.write(res)
	f.close()

	end_time = time.time()
	f2 = open(log_dir + sound_name+'.log', 'w')
	# f2.write(duration+'\n')
	f2.write('Time cost: '+str(end_time - start_time)+'s\n')
	f2.write(stdoutput)
	f2.close()

	# delete_command = 'rm -f '+ sound
	# p2 = subprocess.Popen(delete_command, shell=True)
	# b = p2.wait()
	print(sound_name + ' Completed!')

# @timeit
# def run(video, video_name, video_dir, sound_dir, txt_dir, log_dir):
# 	start_time = time.time()
# 	duration = get_info(video, video_name, video_dir)
# 	sound = dump_wav(video, video_name, video_dir, sound_dir)
# 	asr_run(sound, video_name, txt_dir, log_dir, duration, start_time)
# 	# return duration



if __name__ == '__main__':
	sound = sys.argv[1]
	sound_name = sys.argv[2]
	txt_dir = sys.argv[3]
	log_dir = sys.argv[4]
	asr_run(sound, sound_name, txt_dir, log_dir, duration='1',  start_time=1)


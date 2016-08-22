import sys, time, subprocess
from nltk_extract.extract_stem import *

def word2vec(method, word_path, result_path):
	start = time.time()

	# word_path = './words'
	# result_path = './results'

	with open(word_path, 'r') as f:
		# As the extract_keywords.py would bring another '\n' in the end.
		words = f.read().split('\n')[:-1]
		# print(len(words))
	f.close()
	result = []

	if method == 'msc':
		for word in words:
			cmd = 'curl http://127.0.0.1:5000/word2vec/msc?word=' + word
			p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			r = p.wait()
			(stdoutput, erroutput) = p.communicate()
			stdoutput = stdoutput.decode('utf-8').split('\n')[-2]
			# print(stdoutput.split('\n'))
			if stdoutput == '0':
				word = extract(word)
				cmd = 'curl http://127.0.0.1:5000/word2vec/msc?word=' + word
				p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
				r = p.wait()
				(stdoutput, erroutput) = p.communicate()
				stdoutput = stdoutput.decode('utf-8').split('\n')[-2]
			result.append(stdoutput)
	elif method == 'sc':
		for word in words:
			cmd = 'curl http://127.0.0.1:5000/word2vec/sc?word=' + word
			p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			r = p.wait()
			(stdoutput, erroutput) = p.communicate()
			stdoutput = stdoutput.decode('utf-8').split('\n')[-2]
			# print(stdoutput.split('\n'))
			if stdoutput == '0':
				t1 = time.time()
				word = extract(word)
				t2 = time.time()
				print t2-t1
				cmd = 'curl http://127.0.0.1:5000/word2vec/sc?word=' + word
				p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
				r = p.wait()
				(stdoutput, erroutput) = p.communicate()
				stdoutput = stdoutput.decode('utf-8').split('\n')[-2]
			result.append(stdoutput)
	# print(result)

	with open(result_path, 'w') as f:
		for item in result:
			f.write(item+'\n')
	f.close()

	end = time.time()
	# print(end - start)

if __name__ == '__main__':
	method = sys.argv[1]
	word_path = sys.argv[2]

	if len(sys.argv) == 4:
		result_path = sys.argv[3]
	else:
		result_path = './results'

	word2vec(method, word_path, result_path)
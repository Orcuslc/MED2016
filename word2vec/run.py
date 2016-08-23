# Handle_words:
# The fusion of ../nltk_extract/extract_keywords.py and ./test.py

import sys, os
sys.path.insert(0, '..')

from time import time as t
# from nltk_extract.extract_keywords import extract_
from test import word2vec_
# from nltk_extract.extract_stem import *

method = 'sc'
# method = sys.argv[1]
# sentence_path = sys.argv[2]
keywords_path = sys.argv[2:]
# sentence_name = sys.argv[3]
name_list = [item[-13:] for item in keywords_path]
# tmp_path = sys.argv[4]
result_path = sys.argv[1]

def run(keywords_path, name_list, result_path):
	# print sentence_path+sentence_name
	# t1 = t()
	# extract_(sentence_path+sentence_name, tmp_path+sentence_name)
	# t2 = t()
	keywords_list = []
	for keywords in keywords_path:
		with open(keywords_path) as f:
			keywords_list.append(f.read().split('\n'))
	word2vec_(method, keywords_list, name_list, result_path)
	# t3 = t()
	# print t2-t1, t3-t1

# def run_(sentence_path, result_path):
# 	files = os.listdir(sentence_path)
# 	extract_(sentence_path, result_path)

if __name__ == '__main__':
	s = t()
	run(sentence_path, sentence_name, result_path)
	e = t()
	print(e-s)
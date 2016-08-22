# Handle_words:
# The fusion of ../nltk_extract/extract_keywords.py and ./test.py

import sys, os
sys.path.insert(0, '..')

from time import time as t
from nltk_extract.extract_keywords import extract_
from test import word2vec
# from nltk_extract.extract_stem import *


method = sys.argv[1]
sentence_path = sys.argv[2]
sentence_name = sys.argv[3]
tmp_path = sys.argv[4]
result_path = sys.argv[5]

def run(sentence_path, sentence_name, result_path):
	# print sentence_path+sentence_name
	# t1 = t()
	extract_(sentence_path+sentence_name, tmp_path+sentence_name)
	# t2 = t()
	word2vec(method, tmp_path+sentence_name, result_path+sentence_name)
	# t3 = t()
	# print t2-t1, t3-t1

def run_(sentence_path, result_path):
	files = os.listdir(sentence_path)
	extract_(sentence_path, result_path)

if __name__ == '__main__':
	s = t()
	run(sentence_path, sentence_name, result_path)
	e = t()
	print(e-s)
# Run-extract
from extract_keywords import extract_
import sys

sentence_path = sys.argv[1]
key_words_path = sys.argv[2]

sentence_name = sentence_path[-13:]
key_words_path = key_words_path+sentence_name
extract_(sentence_path, key_words_path)

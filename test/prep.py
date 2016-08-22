import sys, os

method = sys.argv[1]
sentence_path = sys.argv[2]
sentence_name = sys.argv[3]
tmp_path = sys.argv[4]
result_path = sys.argv[5]

sentences = os.listdir(sentence_path)
sentence_names = [item[:-4] for item in sentences]
with open('./sentences', 'w') as f:
	for i in sentence_names:
		f.write(method+' '+sentence_path+' '+i+' '+tmp_path+' '+result_path+'\n')


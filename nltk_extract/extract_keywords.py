import nltk
from nltk.corpus import brown
import sys
# REVISED By Orcuslc for MED2016
# August, 2016
# This is a fast and simple noun phrase extractor (based on NLTK)
# Feel free to use it, just keep a link back to this post
# http://thetokenizer.com/2013/05/09/efficient-way-to-extract-the-main-topics-of-a-sentence/
# Create by Shlomi Babluki
# May, 2013
 
# This is our fast Part of Speech tagger
#############################################################################
brown_train = brown.tagged_sents(categories='news')
regexp_tagger = nltk.RegexpTagger(
	[(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
	 (r'(-|:|;)$', ':'),
	 (r'\'*$', 'MD'),
	 (r'(The|the|A|a|An|an)$', 'AT'),
	 (r'.*able$', 'JJ'),
	 (r'^[A-Z].*$', 'NNP'),
	 (r'.*ness$', 'NN'),
	 (r'.*ly$', 'RB'),
	 (r'.*s$', 'NNS'),
	 (r'.*ing$', 'VBG'),
	 (r'.*ed$', 'VBD'),
	 (r'.*', 'NN')
])
unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)
bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)
#############################################################################
# This is our semi-CFG; Extend it according to your own needs
#############################################################################
cfg = {}
cfg["NNP+NNP"] = "NNP"
cfg["NN+NN"] = "NNI"
cfg["NNI+NN"] = "NNI"
cfg["JJ+JJ"] = "JJ"
cfg["JJ+NN"] = "NNI"
#############################################################################
class NPExtractor(object):
	def __init__(self, sentence):
		self.sentence = sentence
	# Split the sentence into singlw words/tokens
	def tokenize_sentence(self, sentence):
		tokens = nltk.word_tokenize(sentence)
		return tokens
	# Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")
	def normalize_tags(self, tagged):
		n_tagged = []
		for t in tagged:
			if t[1] == "NP-TL" or t[1] == "NP":
				n_tagged.append((t[0], "NNP"))
				continue
			if t[1].endswith("-TL"):
				n_tagged.append((t[0], t[1][:-3]))
				continue
			if t[1].endswith("S"):
				n_tagged.append((t[0], t[1][:-1]))
				continue
			n_tagged.append((t[0], t[1]))
		return n_tagged
	# Extract the main topics from the sentence
	def extract(self):
		tokens = self.tokenize_sentence(self.sentence)
		tags = self.normalize_tags(bigram_tagger.tag(tokens))
		merge = True
		while merge:
			merge = False
			for x in range(0, len(tags) - 1):
				t1 = tags[x]
				t2 = tags[x + 1]
				key = "%s+%s" % (t1[1], t2[1])
				value = cfg.get(key, '')
				if value:
					merge = True
					tags.pop(x)
					tags.pop(x)
					match = "%s %s" % (t1[0], t2[0])
					pos = value
					tags.insert(x, (match, pos))
					break
		matches = []
		for t in tags:
			if t[1] == "NNP" or t[1] == "NNI":
			#if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN":
				matches.append(t[0])
		return matches

# Main method, just run "python np_extractor.py"
# def main():
#     sentence = "Swayy is a beautiful new dashboard for discovering and curating online content."
#     np_extractor = NPExtractor(sentence)
#     result = np_extractor.extract()
#     print ("This sentence is about: %s" % ", ".join(result))

def handle_sentence(sentence):
	nonsense = ['uh', 'huh', 'mm', 'uh-huh', 'mhm', 'I', "I'm", 'oh', 'i', "i'm", 'um']
	sound = ['[noise]', '[laughter]']
	words = sentence.split(' ')
	nsentence = []
	for word in words:
		if word not in nonsense:
			if word not in sound:
				nsentence.append(word)
			else:
				word = word[1:-1]
				nsentence.append(word)
	return ' '.join(nsentence)


def extract_(sentence_path, key_words_path):
	with open(sentence_path) as f:
		sentence = f.read()
	f.close()
	sentence = handle_sentence(sentence)
	print(sentence)
	np_extractor = NPExtractor(sentence)
	result = np_extractor.extract()
	print result
	with open(key_words_path, 'w') as f:
		for word in result:
			words = word.split(' ')
			for single_word in words:
				f.write(single_word+'\n')

# def extract__(sentence_path, file_names, result_path):
# 	res = []
# 	for name in file_names:
# 		with open(sentence_path+name) as f:
# 			sentence = f.read()
# 		f.close()
# 		np_extractor = NPExtractor(sentence)
# 		result = np_extractor.extract()


if __name__ == '__main__':
	# main()
	sentence_path = sys.argv[1]
	result_path = sys.argv[2]

	
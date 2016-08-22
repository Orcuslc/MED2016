from nltk.stem import *

wnl = WordNetLemmatizer()
# prt = porter.PorterStemmer()

def extract(word):
	return wnl.lemmatize(word)
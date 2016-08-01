import os
import sys

rootdir = '/home/orcuslc/MED/TIMIT'
for parent, dirs, files in os.walk(rootdir):
	for file in files:
		print(file)
		if file[:10] == 'index.html':
			os.remove(os.path.join(parent, file))

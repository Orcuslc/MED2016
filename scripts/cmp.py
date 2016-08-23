import numpy as np
import os,sys

txt_list = os.listdir('./txt')
txt_name = [item[:-4] for item in txt_list]
sound_list = os.listdir('./sound')
diff = []
for item in sound_list:
        name = item[-13:-4]
        if name not in txt_name:
                diff.append(item)
with open('diff', 'w') as f:
        for i in diff:
                f.write('./sound/'+i+'\n')


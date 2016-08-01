import os

path = '/home/orcuslc/MED/TIMIT'

def rename_dir(path):
    for filename in os.listdir(path):
        oldpath = path+'/'+filename
        newpath = path+'/'+filename.upper()
        if os.path.isdir(oldpath):
            os.rename(oldpath, newpath)
            rename_dir(newpath)

rename_dir(path)

import os

def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        
def file_w(path, data):
    f = open(path,'w')
    f.write(data)
    f.close()
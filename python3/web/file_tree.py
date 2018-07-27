import urllib.request
import urllib.error
import os
import queue
import argparse
from threading import *

def test_remote(tgt,paths):
	while not paths.empty():
		path = paths.get() #get item from queue
		url = "{0}{1}".format(tgt, path) #get query url

		request = urllib.request.Request(url)

		try:
			response = urllib.request.urlopen(request)
			content = response.read()

			print("[{0}} to {1}".format(response.code, path))
		except urllib.error.HTTPError as error:
			print("Error: {1}", error.code)

def main():
	parser = argparse.ArgumentParser(description = "Sniffer,scanner")
	parser.add_argument("-t",action="store",dest="tgt",help="remote target website")
	parser.add_argument("-d",action="store",dest="dir",help="directory")
	results = parser.parse_args()

	if results.tgt is None or results.dir is None:
		parser.print_help()
		exit(0)

	tgt = results.tgt #define remote target website
	dir_ = results.dir #directory

	thread_lmt = 10
	flt = [".jpg", ".gif", ".png", ".css"] #filters

	os.chdir(dir_)

	paths = queue.Queue()

	for dirpath,dirnames,filenames in os.walk('.'):
		for f in filenames:
			remote_path = os.path.join(dirpath, f) #file path
			if remote_path.startswith("."):
				remote_path = remote_path[1:] # remove period
			if os.path.splitext(f)[1] not in flt:
				paths.put(remote_path)

	for i in range(0, thread_lmt):
		print("Thread number: {0}".format(i))
		t = Thread(target=test_remote,args=(tgt,paths))
		t.start()

if __name__ == '__main__':
	main()
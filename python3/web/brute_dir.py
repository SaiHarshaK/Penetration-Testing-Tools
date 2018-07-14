'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	Brute force directories
	Use	 	:	to find configurational files, debuggging scripts, etc for any vulnerabilities 
'''

import urllib.error
import urllib.request
import queue
from threading import *

def wordlist(file,check_resume):
	# read in the wordlist
	f = open(file, "r")
	raw_words = f.readlines()
	f.close()

	resume = False
	words = queue.Queue()
	
	for word in raw_words:
		word = word.strip()
		if check_resume is not None:
			if resume:
				words.put(word)
			else:
				if word == check_resume:
					resume = True
					print("[*]Resuming wordlist from: {0}".format(check_resume))
		else:
			words.put(word)
	return words

def brute_dir(queue_words, extn=None):
	while not queue_words.empty():
		try_brute = word_queue.get()
		brute_list = []
		
		# check if there's a file extension, if there is not, it's a 
		# directory we're bruting
		if '.' not in try_brute:
			brute_list.append("/{0}/".format(try_brute))
		else:
			brute_list.append("/{0}".format(try_brute))
		# check if we want to bruteforce extensions
		if extn is not None:
			for extension in extn:
				brute_list.append("/{0}{1}".format(try_brute, extension))
		# iterate over our list of attempts
		for brute in brute_list:
			url = "{0}{1}".format(url, urllib.request.quote(brute))
			try:
				headers = {"User-Agent":user_agent}
				r = urllib.request.Request(url, headers=headers)
				response = urllib.request.urlopen(r)
				if len(response.read()):
					print("[*][{0}] :  {1}".format(response.code, url))
			except urllib.error.URLError as e:
				if hasattr(e, "code") and e.code != 404:
					print("[*]{0} : {1}".format(e.code, url))
				pass
def main():
	parser = argparse.ArgumentParser(description = "Brute force directories")
	parser.add_argument("-t",action="store",dest="url",help="target url")
	results = parser.parse_args()

	if results.url is None:
		parser.print_help()
		exit(0)

	thread_lmt = 50
	url = results.url
	file = "all.txt" #containing wordlists, from SVNDigger
	check_resume = None #if any network connectivity issue
	user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"

	queue_words = wordlist(file,check_resume)
	extn = [".php", ".bak", ".orig", ".inc"]
	for i in range(0, thread_lmt):
		t = Thread(target=brute_dir, args=(queue_words, extn,))
		t.start()

if __name__ == '__main__':
	main()
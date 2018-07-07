'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	Unix password Cracker, implementing Dictionary attack from "dict.txt" by taking input from "pwd.txt".
	Use	 	:	returns password if found.
	Usage	:	python3 uPwdCrack.py -p <passwordFile> -d <dictionaryFile>
	format	
	in txt	:	id: encrypted_password
	file
'''

import crypt
import argparse

# returns password if found
def findPwd(encrypted,dictionaryFile):
	salt = encrypted[0:2] # first two bytes is equal to salt
	try:
		dictFile = open(dictionaryFile)
		for word in dictFile.readlines():
			word1 = word.strip('\n')
			eWord = crypt.crypt(word1,salt)
			eWord = eWord.strip('.')
			if (encrypted == eWord):
				print("[*] password is : "+word1+'\n')
				dictFile.close()
				return
	except Exception as e:
		print(e)
		dictFile.close()
		return

	print("[*] password not found.\n")# file is exhausted
	dictFile.close()
	return

def main():
	parser = argparse.ArgumentParser(description = "Unix password Cracker")
	parser.add_argument("-p",action="store",dest="passwordFile",help="the file contaning unix encrypted passwords")
	parser.add_argument("-d",action="store",dest="dictionaryFile",help="the file contaning dictionary")
	results = parser.parse_args()
	if (results.zFile == None) or (results.dictionaryFile == None):
		parser.print_help()
		exit(0)
	
	pwdFile = open(str(results.passwordFile))
	for line in pwdFile.readlines():
		if ':' in line:
			ids = line.split(':')[0]
			encrypted = line.split(':')[1].strip(' ')
			print("Finding password for : "+ids)
			findPwd(encrypted.strip('\n'),str(results.dictionaryFile))
	pwdFile.close()

if __name__ == "__main__":
	main()
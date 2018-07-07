'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	zip File password Cracker, implementing Dictionary attack from "dict.txt"(or add list of trials manually).
	Usage	:	python3 uPwdCrack.py -p <passwordFile> -d <dictionaryFile>
	Use 	:	extarcts contents of file if password is found
	
'''
#only for zipcrypto based encryption
import zipfile
import argparse
from threading import Thread

#extract if right password given
def extract(zFile,passwd):
	try:
		zFile.extractall(pwd=b'passwd')
		print("[*] Password is : "+passwd)
		return
	except Exception as e:
		print(e)
		return

def main():
	parser = argparse.ArgumentParser(description = "Zip File password Cracker")
	parser.add_argument("-z",action="store",dest="zFile",help="the zip file")
	parser.add_argument("-d",action="store",dest="dictionaryFile",help="the file contaning dictionary")
	results = parser.parse_args()
	if (results.zFile == None) or (results.dictionaryFile == None):
		parser.print_help()
		exit(0)

	results.zFile = zipfile.ZipFile(str(results.zFile)) #open zip file using "zFile" name.
	pwdFile = open(str(results.dictionaryFile))
	print(str(results.dictionaryFile),len(str(results.dictionaryFile)))
	print(str(results.zFile),len(str(results.zFile)))

	for line in pwdFile.readlines():
		pwd = line.strip('\n')
		t = Thread(target=extract,args=(results.zFile,pwd))
		t.start()
		extract(results.zFile,"egg")

	pwdFile.close()

if __name__ == "__main__":
	main()
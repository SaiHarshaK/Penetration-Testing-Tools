'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	TCP Port Scanner + banner grabbing
	Use	 	:	identify hosts using TCP full connect scan
'''

import socket
import argparse
from threading import *

#grab banner
screenLock = Semaphore(value = 1)
def connectPort(host,port):
	try:
		s = socket.socket()
		s.connect((host,port))
		s.send(b"hi\n")
		result = s.recv(100)
		screenLock.acquire()
		print("[+]"+str(port)+" is open")
		print("[+]Banner : "+str(result))
		s.close()		
	except:
		screenLock.acquire()
		print("[-]"+str(port)+" is closed")
	finally:
		screenLock.release()

#get hostname and traverse through individual ports.
def portScan(host,ports):
	try:
		ip = socket.gethostbyname(host)
	except:
		print("[-]cannot resolve Host")
		return

	try:
		name = socket.gethostbyaddr(ip)
		print("[*]Scanning "+name[0])
	except:
		print("[*]Scanning "+ip)


	for port in ports:
		t = Thread(target=connectPort,args=(host,int(port)))
		t.start()

def main():
	parser = argparse.ArgumentParser(description = "TCP port scanner + banner grabbing")
	parser.add_argument("--host",action="store",dest="host",help="target host")
	parser.add_argument("-p",action="store",dest="ports",nargs='+',type=int,help="target port[s]")
	results = parser.parse_args()

	if (results.host == None) or (results.ports[0] == None):
		parser.print_help()
		exit(0)

	portScan(results.host,results.ports)

if __name__ == "__main__":
	main()
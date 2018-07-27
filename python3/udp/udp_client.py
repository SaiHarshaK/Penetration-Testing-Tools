'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	UDP client
	Use	 	:	test for services , send data, etc(similar to TCP client)
'''

import socket
import argparse

def main()
	parser = argparse.ArgumentParser(description = "UDP client")
	parser.add_argument("--host",action="store",dest="host_",help="target host")
	parser.add_argument("-p",action="store",dest="port_",type=int,help="target port")
	results = parser.parse_args()

	if (results.host_ == None) or (results.port_ == None):
		parser.print_help()
		exit(0)

	data = input("any data to be sent?")
	#create socket
	s = socket.socket((socket.AF_INET, socket.SOCK_DGRAM) #different socket type comapred to tcp
	#no need to call connect since UDP is a connectionless protocol
	s.sendto(data.encode("utf-8"),(host,port))
	data,addr = s.recvfrom(4096)

	print(data)

if __name__ == "__main__":
	main()
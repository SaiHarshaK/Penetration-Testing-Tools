'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	TCP Client
	Use	 	:	test for services , send data, etc
'''

import socket
import argparse

def main():
	parser = argparse.ArgumentParser(description = "TCP client")
	parser.add_argument("--host",action="store",dest="host_",help="target host")
	parser.add_argument("-p",action="store",dest="port_",type=int,help="target port")
	results = parser.parse_args()

	if (results.host_ == None) or (results.port_ == None):
		parser.print_help()
		exit(0)

	host = results.host_
	port = results.port_

	data = input("any data to be sent?\n")

	#create socket
	s = socket.socket()
	s.connect((host,int(port)))
	s.send(data.encode("utf-8"))
	
	resp = "" #response
	while True:
		resp += s.recv(1024).decode("utf-8") #response
		if s.recv(1024) < 1024:
			break 
		
	print(resp)

if __name__ == "__main__":
	main()
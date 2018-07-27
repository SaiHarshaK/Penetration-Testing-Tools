'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	TCP Server
	Use	 	:	for command shells or proxy
'''

import socket
import argparse
from threading import Thread

def handler(s_client):
	resp = s_client.recv(1024).decode("utf-8") #response
	print("[*]Received: %s " % resp)

	s_client.send(b"hi")
	s_client.close()
	return

def main():
	ip = "0.0.0.0"
	port = 9999

	server = socket.socket()

	server.bind((ip,port))
	server.listen(5)
	print("[*]Listening on %s:%d" %(ip,port))

	while True:
		host, addr = server.accept()
		print("[*]Connected to %s:%d" % (addr[0],addr[1]))

	#threading
	t = Thread(target = handler, args = (host,))
	t.start()

if __name__ == "__main__":
	main()
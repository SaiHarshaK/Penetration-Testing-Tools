'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	TCP Proxy
	Use	 	:	to help understand unknown protocols, create test cases for fuzzers and modify traffic being sent to an application
'''

import sys
import socket
from threading import Thread
import argparse

def request(buffer_):
	# write code for packet modifications
	return buffer_

def response(buffer_):
	# write code for packet modification
	return buffer_

def receive_from(connection):
	buffer_ = "".encode("utf-8") #buffer

	connection.settimeout(5)
	try:
		# read data till timeout
		while True:
			data = connection.recv(1024)
			if not data:
				break
			buffer_ += data
	except Exception as e:
		print(e)
		
	return buffer_

#inspect and retrieve info
#useful for unknown protocols,finding user credentials,etc
def hexdump(src, length=16):
	result=[]
	if isinstance(src,str):
		digits = 4
	else:
		digits = 2

	for c in range(0,len(src),length):
		source = src[c:c+length]
		hexa = b' '.join(["%0*X".encode() % (digits, ord(x)) for x in source])
		text = b''.join([x.encode() if 0x20 <= ord(x) < 0x7F else b'.' for x in source])
		result.append(b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text))

	print(b'\n'.join(result))

#responsible for sending and receiving data to either side of data stream
def proxy(s_client,host_remote,port_remote,receive):
	s_remote = socket.socket()
	s.connect((host_remote,port_remote))

	#check before going to main loop(necessary for FTP like servers)
	if receive:
		r_buffer = receive_from(s_remote) #remote buffer
		#check
		hexdump(r_buffer)
		r_buffer = response(r_buffer)
		
		#send data?
		if len(r_buffer):
			print("[*]Sending %d bytes" % len(r_buffer))
			s_client.send(r_buffer)
	#read from local host and sent to remote and local hosts
	while True:
		l_buffer = receive_from(s_client) #local buffer

		#received data?
		if len(l_buffer):
			print("[*]Received %d bytes" % len(l_buffer))
			hexdump(l_buffer.decode("utf-8","ignore"))#check

		l_buffer = request(l_buffer)
		s_remote.send(l_buffer)
		print("[*]Successfully sent to remote")
		
		r_buffer = receive_from(s_remote)

		if len(r_buffer):
			print("[*]Received %d bytes from remote" % len(r_buffer))
			hexdump(r_buffer.decode("utf-8","ignore"))#check

			r_buffer = response(r_buffer) #get response
			s_client.send(r_buffer) #send response
			print("[*]Sent -> local client")

		#work done?
		if len(l_buffer) == 0 and len(r_buffer) == 0:
			s_client.close()
			s_remote.close()
			print("[*]Closing connections")
			break


def server_loop(host_local,port_local,host_remote,port_remote,receive):
	server = socket.socket()
	try:
		server.bind((host_local,port_local))
	except:
		print("[-]failed to access {0}:{1}".format(host_local,port_local))
		exit(0)
	
	print("[*]Listening on %s:%d" % (host_local,port_local))
	server.listen(5)

	while True:
		s_client, addr = server.accept()
		print("[*]Connected to {0}:{1}".format(addr[0],addr[1]))

		#connection to remote host
		t = Thread(target = proxy,args = (s_client,host_remote,port_remote,receive))
		t.start()

def main():
	parser = argparse.ArgumentParser(description = "TCP proxy")
	parser.add_argument("-lh",action="store",dest="host_local_",help="local host ")
	parser.add_argument("-lp",action="store",dest="port_local_",type=int,help="local port")
	parser.add_argument("-rh",action="store",dest="host_remote_",help="remote host")
	parser.add_argument("-rp",action="store",dest="port_remote_",type=int,help="remote port")
	parser.add_argument("-r",action="store_true",help="receive data before sending to remote host")
	results = parser.parse_args()
	#local
	host_local = results.host_local_
	port_local = results.port_local_
	#remote
	host_remote = results.host_remote_
	port_remote = results.port_remote_
	#receive?
	receive = results.r
	# to listen connections
	server_loop(host_local,port_local,host_remote,port_remote,receive)

if __name__ == "__main__":
	main()
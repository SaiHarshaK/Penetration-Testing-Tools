'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	Net tool,Netcat alternative in python
	Use	 	:	a simple network client and server that you can use to push files, or to have a listener that gives you
				command-line access.
'''

import sys
import socket
import argparse
from threading import *
import subprocess

#global
listen = False
command = False
execute = ""
target = ""
up_Destn = "" # upload destination
port = 0


def handler(s_client):
	global command
	global execute
	global up_Destn
	#for file uploads
	if len(up_Destn):
		print("[*]In file upload!")
		f_buffer="" # file buffer

		while True:
			data = s_client.recv(1024).decode("utf-8")
			if not data:
				break
			else:
				file_buff += data

		#write data
		try:
			#binary mode, for binary executables
			file = open(up_Destn,"wb")
			file.write(f_buffer)
			file.close()

			#confirm that we have written the file
			resp = "[+]saved file to : "+up_Destn
			s_client.send(resp.encode("utf-8"))
		except:
			resp = "[-]Failed to save file to : "+up_Destn
			s_client.send(resp.encode("utf-8"))

	#command execute
	if len(execute):
		print("[*]To Execute..")
		output = execute_cmd(execute)
		#execute and send the result
		s_client.send(output.encode("utf-8"))
	#command shell
	if command:
		print("[*]Entering Shell")
		while True:
			# a prompt
			try:
				s_client.send("<NT:$> ".encode("utf-8"))
			except Exception as e:
				print(e)

			cmd_buffer = ""
			#stop when '\n' is pressed
			while '\n' not in cmd_buffer:
				cmd_buffer += s_client.recv(1024).decode("utf-8")

			resp = execute_cmd(cmd_buffer)
			# resp is in bytes now

			#send response
			s_client.send(resp)

#primary server loop
def server_loop():
	print("[*]In server loop!")
	global host
	global port

	#if no host, we listen on all interfaces
	if host is None:
		host = "0.0.0.0"
	server = socket.socket()
	server.bind((host,port))

	server.listen(5)

	while True:
		s_client,addr = server.accept() # client socket

		t = Thread(target=handler,args=(s_client,))
		t.start()

def execute_cmd(command):
	command = command.rstrip()
	print("Executing: %s" % command)
	try:
		output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
	except:
		output = "[-]Error executing command\r\n"
	finally:
		return output

def client_send(cmd_buffer):
	global host
	global port
	print("[*]Sending data to client on port %d" % port)
	tgt_client = socket.socket() # target client
	try:
		tgt_client.connect((host,port))

		#if we received any buffer
		if len(cmd_buffer):
			tgt_client.send(cmd_buffer.encode("utf-8"))
		#continue sending and receiver until user stops it
		
		#flag = 1 
		while True:
			len_recv = 1 # length of data we receive
			resp = "" # response
			while len_recv:
				print("[*]Waiting for response from client!")
				data = tgt_client.recv(1024)
				resp += data.decode("utf-8",errors="ignore")
				#fkin utf-8 cant decode 0x0a

				if len(data) < 1024:
					break

			print("[*]"+resp,end="")

			#get input
			cmd_buffer = input("")
			cmd_buffer += '\n'

			tgt_client.send(cmd_buffer.encode("utf-8"))
			'''
			if flag is 1:
				tgt_client.send('\n'.encode("utf-8"))
				flag = 0
			'''
	except:
		print("[*]Exiting!")
	finally:
		tgt_client.close()

def main():
	global listen
	global command
	global execute
	global host
	global up_Destn
	global port

	parser = argparse.ArgumentParser(description = "Net tool,Netcat alternative in python")
	parser.add_argument("--host",action="store",dest="host_",help="target host")
	parser.add_argument("-p",action="store",dest="port_",type=int,help="target port")
	parser.add_argument("-l",action="store_true",help="listen host:port for incoming connections")
	parser.add_argument("-c",action="store_true",help="start command shell")
	parser.add_argument("-e",action="store",dest="exec",help="execute file if connected")
	parser.add_argument("-u",action="store",dest="up",help="upload destination to upload and write file")
	results = parser.parse_args()

	listen = results.l
	command = results.c
	host = results.host_
	if results.up != None:
		up_Destn = results.up
	if results.exec != None:
		execute = results.exec
	if results.port_ != None:
		port = results.port_

	if not listen and results.host_ != None and results.port_ != None:
		#read buffer from commandline
		#ctrl-D (for EOF)
		cmd_buffer = sys.stdin.read()
		#send data
		client_send(cmd_buffer)

	if listen:
		server_loop()

if __name__ == "__main__":
	main()
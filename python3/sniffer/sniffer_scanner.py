'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	Sniffer,scanner
	Use	 	:	Serves as a UDP Host discovery Tool on network. 
'''

import os
import socket
import sys
import struct
import argparse
import time
from netaddr import IPNetwork,IPAddress
from threading import *
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

	#form structure
	def __new__(self, socket_buffer=None):
		return self.from_buffer_copy(socket_buffer)
	#human readable output
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

class ICMP(Structure):
    _fields_ = [
        ("type", c_ubyte),
        ("code", c_ubyte),
        ("checksum", c_ushort),
        ("unused", c_ushort),
        ("next_hop_mtu", c_ushort)
    ]
    
    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer):
        pass

def udp_sender(subnet, msg):
	time.sleep(5)
	sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	for ip in IPNetwork(subnet):
		try:
			sender.sendto(msg.encode("utf-8"), (str(ip), 65210))
		except:
			print("Exception encountered in udp_sender")
			
	print("UDP packets sent successfully")

def main():
	parser = argparse.ArgumentParser(description = "Sniffer,scanner")
	parser.add_argument("--host",action="store",dest="host_",help="host to listen on")
	parser.add_argument("-s",action="store",dest="subnet",help="subnet to target")
	results = parser.parse_args()

	if results.host_ is None or results.subnet is None:
		parser.print_help()
		exit(0)

	host = results.host_
	subnet = results.subnet

	#string to be searched
	msg = "yolo!" 

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

	# send packets
	t = Thread(target=udp_sender, args=(subnet, msg))
	t.start()

	try:
		while True:
			# read packet in bytes
			raw_buffer = sniffer.recvfrom(65565)[0] # for bytes
			# get IP header from the first 20 bytes
			iph = IP(raw_buffer[0:20])
			
			#uncomment to check protocols and hosts
			#print("[*]Protocol: {0} {1} to{2}".format(iph.protocol, iph.src_address, iph.dst_address))

			if iph.protocol == "ICMP":
				# find where ICMP packet starts
				offset = iph.ihl * 4
				buffer_ = raw_buffer[offset:offset + sizeof(ICMP)]

				# ICMP structure
				icmph = ICMP(buffer_) #ICMP header

				#uncomment to check values
				#print("[*]ICMP -> Type: {0} Code: {1}".format(icmph.type, icmph.code))

				#port unreachable and destination unreachable respectively
				if icmph.code == 3 and icmph.type == 3:
					# verify host is target subnet
					if IPAddress(iph.src_address) in IPNetwork(subnet):
						# check for message
						if raw_buffer[len(raw_buffer)-len(msg):] == msg.encode("utf-8"):
							print("Host Active: {0}".format(ip_header.src_address))


	except KeyboardInterrupt:
		# # if windows, switch off promuscous mode
		if os.name == "nt":
			sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)	

if __name__ == "__main__":
	main()
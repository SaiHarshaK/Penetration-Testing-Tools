'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	Port scanner with nmap
	Required:	nmap module
	Use	 	:	identify hosts with nmap
'''

import argparse
import nmap
from threading import *

#grab banner
screenLock = Semaphore(value = 1)

#get hostname and traverse through individual ports.
def nmapScan(host,port):
	n_scan = nmap.PortScanner()
	n_scan.scan(host,port)
	state = n_scan[host]['tcp'][int(port)]['state']
	print("[+] " +host + " port :" + port + " " + state)

def main():
	parser = argparse.ArgumentParser(description = "Port Scanner with NMAP")
	parser.add_argument("--host",action="store",dest="host",help="target host")
	parser.add_argument("-p",action="store",dest="ports",nargs='+',type=int,help="target port[s]")
	results = parser.parse_args()

	if (results.host == None) or (results.ports[0] == None):
		parser.print_help()
		exit(0)

	for port in results.ports:
		nmapScan(results.host,port)

if __name__ == "__main__":
	main()
#example: $python3 main.py -d <directory name> -c "<nmap options>""  -t <url>

import sys
import argparse
from os_make_files import *
from domain import *
from ip_addr import *
from robots import *
from cmd_nmap import *
from cmd_whois import *

def main():
	root = 'scanned'#all scanned websites details go here
	make_dir(root)

	parser = argparse.ArgumentParser(description = "Scanner")
	parser.add_argument("-d",action="store",dest="dir",help="name of directory")
	parser.add_argument("-t",action="store",dest="tgt",help="Url")
	results = parser.parse_args()

	if results.dir is None  or results.tgt is None:
		parser.print_help()
		exit(0)

	nmap_cmd = input("Enter nmap option : ")
	scan(results.dir,nmap_cmd,results.tgt,root)

def scan(name, cmd, url, root):
	domain = domain_name(url)
	ip = ip_addr(domain)
	nmap = get_nmap(str(cmd), ip)
	robots_txt = robots(url)
	who = cmd_whois (domain)
	create_report(name, url, domain, robots_txt, nmap, who, root)

def create_report(name, url, domain, robots_txt, nmap, who , root):
	main_dir = root + '/' + name
	make_dir(main_dir)
	file_w(main_dir + '/url_full.txt', url)
	file_w(main_dir + '/domain.txt', domain)
	file_w(main_dir + '/robots.txt', robots_txt.decode())
	file_w(main_dir + '/cmd_nmap.txt', nmap)
	file_w(main_dir + '/cmd_whois.txt', who)


if __name__ == '__main__':
	main()
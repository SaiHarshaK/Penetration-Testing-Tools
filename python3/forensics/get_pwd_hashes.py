'''
	Tested on python3
	About	: Hashed password grabber
	pre-req : volatility library library(https://code.google.com/p/volatility/downloads/list)
'''

import sys
import struct
import argparse
import volatility.conf as conf
import volatility.registry as registry
import volatility.commands as commands
import volatility.addrspace as addrspace
from volatility.plugins.registry.registryapi import RegistryApi
from volatility.plugins.registry.lsadump import HashDump

def main():
	parser = argparse.ArgumentParser(description = "Hashed password grabber")
	parser.add_argument("-mf",action="store",dest="file",help="memory file(.vmem)")
	parser.add_argument("-p",action="store",dest="path",type=int,help="path to volatility")
	results = parser.parse_args()

	if results.file is None or results.path is None:
		parser.print_help()
		exit(0)

	memory_file = results.file #.vmem
	sys.path.append(results.path)
	registry.PluginImporter()
	config = conf.ConfObject()
	config.parse_options()
	config.PROFILE = "WinXPSP2x86"
	config.LOCATION = "file://{0}".format(memory_file)

	registry.register_global_options(config,commands.Command)
	registry.register_global_options(config,addrspace.BaseAddressSpace)

	registry = RegistryApi(config)
	registry.populate_offsets()

	sam_offset = None
	sys_offset = None

	for offset in registry.all_offsets:
	    if  registry.all_offsets[offset].endswith("\\SAM"):
	        sam_offset  = offset
	        print("[*]SAM: 0x%08x".format(offset))

	    if  registry.all_offsets[offset].endswith("\\system"):
	        sys_offset  = offset
	        print("[*]System: 0x%08x".format(offset))

	    if sam_offset is not None and sys_offset is not None:
	        config.sys_offset = sys_offset
	        config.sam_offset = sam_offset

	        hashdump = HashDump(config)

	        for hash in hashdump.calculate():
	            print(hash)

	        break

	    if sam_offset is None or sys_offset is None:
	print("[*]Failed to find the system or SAM offset.")

if __name__ == '__main__':
	main()
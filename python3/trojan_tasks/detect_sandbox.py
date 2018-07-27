'''
	Tested on python3
	About	: 	Detect sandbox 
'''

import ctypes
import random
import time
import sys

user32=ctypes.windll.user32
kernel32=ctypes.windll.kernel32

keystrokes=0
mouse_clicks=0
double_clicks=0

class LASTINPUTINFO(ctypes.Structure):
	_fields_ = [("cbSize",ctypes.c_uint),("dwTime",ctypes.c_ulong)]

def recent_input():
	struct_lastinputinfo = LASTINPUTINFO()
	struct_lastinputinfo.cbSize = ctypes.sizeof(LASTINPUTINFO)
	user32.GetLastInputInfo(ctypes.byref(struct_lastinputinfo))
	run_time = kernel32.GetTickCount()

	elapsed_time = run_time - struct_lastinputinfo.dwTime

	print("[*]Time elapsed_time since last event(in ms):{0}".format(elapsed_time))

	return elapsed_time

def press_key():
	global mouse_clicks
	global keystrokes

	for i in range(0,0xff):
		if user32.GetAsyncKeyState(i) == -32767:
			#left mouse
			if i == 0x1:
				mouse_clicks += 1
				return time.time()
			elif i > 32 and i < 127:
				keystrokes += 1

	return None

def sandbox_detection():
	global  mouse_clicks
	global  keystrokes

	max_keystrokes = random.randint(10,25)
	max_mouse_clicks = random.randint(5,25)

	double_clicks = 0
	dc_max = 10 #maximum number of double clicks
	dc_threshold = 0.250 #seconds, threshold for double clicks
	dc_first = None #for timestamp of first click of the "dc"

	avg_use_mouse=0
	max_input_threshold=30000 #in milli-seconds

	previous_timestamp=None
	detection_status=False

	last_input = recent_input()

	#threshold limit
	if last_input >= max_input_threshold:
		sys.exit(0)

	while not detection_status:
		time_keypress=press_key()

		if time_keypress is not None and previous_timestamp is not None:
			#time btw double click
			elapsed_time=time_keypress - previous_timestamp

			#double-click
			if elapsed_time <= dc_threshold:
				double_clicks += 1

				if dc_first is None:
					#first click time-stamp
					dc_first = time.time()

				else:
					if double_clicks == dc_max:
						if time_keypress - dc_first <= (dc_max * dc_threshold):
							sys.exit(0)
			#limit
			if keystrokes >= max_keystrokes and double_clicks >= dc_max and mouse_clicks >= max_mouse_clicks:
				return
			
			previous_timestamp=time_keypress
		elif time_keypress is not None:
			previous_timestamp = time_keypress

sandbox_detection()
print("No problems till now!")
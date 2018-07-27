'''
	Tested on python3
	About	: 	Screen Shot Grabber 
'''

import win32gui
import win32ui
import win32con
import win32api

#handle
h_desktop=win32gui.GetDesktopWindow()

#display size
width=win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height=win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left_side=win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top_side=win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

#device context
context_desktop=win32gui.GetWindowDC(h_desktop)
context_image=win32ui.CreateDCFromHandle(context_desktop)

#memory based device context
mem_dc=context_image.CreateCompatibleDC()

ss=win32ui.CreateBitmap() #screenshot
ss.CreateCompatibleBitmap(context_image,width,height)
context_memory.SelectObject(ss)

#copy the screen
context_memory.BitBlt((0,0),(width,height),context_image,(left_side,top_side),win32con.SRCCOPY)

#save
ss.SaveBitmapFile(context_memory,'G:\\Temp\\screenshot.bmp')

#free
context_memory.DeleteDC()
win32gui.DeleteObject(ss.GetHandle())
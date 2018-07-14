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
desktop_dc=win32gui.GetWindowDC(h_desktop)
img_dc=win32ui.CreateDCFromHandle(desktop_dc)

#momory based device context
mem_dc=img_dc.CreateCompatibleDC()

screenshot=win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_dc,width,height)
mem_dc.SelectObject(screenshot)

#copy the screen
mem_dc.BitBlt((0,0),(width,height),img_dc,(left_side,top_side),win32con.SRCCOPY)

#save
screenshot.SaveBitmapFile(mem_dc,'G:\\Temp\\screenshot.bmp')

#free
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())
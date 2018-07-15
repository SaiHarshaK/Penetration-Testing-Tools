'''
	Tested on python3
	About	: Process Monitor with WMI	
	pre-req : pywin32 wmi(http://sourceforge.net/projects/pywin32/)
			  common set of vulnerabilities(http://www.nostarch.com/blackhatpython/ http://www.nostarch.com/blackhatpython/)
'''

import win32con
import win32api
import win32security

import wmi
import sys
import os

def priviledge_process(pid):
    try:
        #process handle
        h_proc = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION,False,pid)

        #process token
        proc_token = win32security.OpenProcessToken(h_proc,win32con.TOKEN_QUERY)


        #priviledge list
        priv = win32security.GetTokenInformation(proc_token,win32security.TokenPrivileges)

        #output enabled ones
        priv_list=""
        for i in priv:
            #enabled?
            if i[1] == 3:
                priv_list += "{0}|".format(win32security.LookupPrivilegeName(None,i[0]))

    except Exception as e:
        print(e)
        priv_list = "N/A"

    return priv_list


def log_file(message):
    with open("process_monitor_log.csv","ab") as f:
        f.write(("{0}\r\n".format(message)).encode("utf-8"))

    return

log_file("Time,User,Executable,CommandLine,PID,Parent PID,Privileges")

w = wmi.WMI()
#process monitor
monitor_process = w.Win32_Process.watch_for("creation")

while True:
    try:
        new_proc = monitor_process()

        proc_owner  = new_proc.GetOwner()
        proc_owner  = "{0}\\{1}".format(proc_owner[0],proc_owner[2])
        date = new_proc.CreationDate
        executable  = new_proc.ExecutablePath
        cmdline     = new_proc.CommandLine
        pid         = new_proc.ProcessId
        parent_id   = new_proc.ParentProcessId
        privileges  = priviledge_process(pid)

        log_process = "{0},{1},{2},{3},{4},{5},{6}\r\n".format(date,proc_owner,executable,cmdline,pid,parent_id,privileges)

        print(log_process)

        log_file(log_process)

    except:
		pass
import os

def get_nmap(options, ip):
    cmd = "nmap " + options + " " + ip
    proc = os.popen(cmd)
    results = str(proc.read())
    return results
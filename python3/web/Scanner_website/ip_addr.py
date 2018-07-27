import os

def ip_addr(url):
    cmd = "host " + url
    proc = os.popen(cmd)
    ip_addr = str(proc.read()).split()[3]
    return ip_addr

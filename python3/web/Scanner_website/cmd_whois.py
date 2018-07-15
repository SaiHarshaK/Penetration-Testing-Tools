import os

def cmd_whois(url):
    cmd = "whois " + url
    proc = os.popen(cmd)
    results = str(proc.read())
    return results
import urllib.request
import io

def robots(url):
    if url.endswith('/'):
        path = url
    else:
        path = url + '/'
    req = urllib.request.Request(path + "robots.txt", data = None) #request
    resp = urllib.request.urlopen(req) #response
    data = resp.read()
    return data
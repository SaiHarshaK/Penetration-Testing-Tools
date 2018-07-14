'''
	Made By Sai Harsha Kottapalli
	Tested on python3
	About	: 	image finder, face recognition
	Use	 	:	Get image files and detect faces from pcap
'''

import re
import zlib
import cv2
from scapy.all import *

def http_headers(payload):
	try:
		headers_raw = payload[:payload.index("\r\n\r\n")+2]
		#get headers
		headers = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", headers_raw))
	except:
		return None

	if("Content-Type" not in headers):
		return None

	return headers

def get_image(headers,payload):
	image=None
	image_type=None

	try:
		if("image" in headers['Content-Type']):
			image_type = headers['Content-Type'].split('/')[1]
			image = payload[payload.index("\r\n\r\n")+4:]

			#decompress if any compression
			try:
				if("Content-Encoding" in headers.keys()):
					if(headers['Content-Encoding']=="gzip"):
						image=zlib.decompress(image,16+zlib.MAX_WBITS)
					elif(headers['Content-Encoding']=="deflate"):
						image=zlib.decompress(image)

			except:
				pass
	except:
		return None,None
	return image,image_type

def face_recog(path,file,f_dir,pcap):
	img = cv2.imread(path)
	cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
	rects = cascade.detectMultuScale(img,1.3,4,cv2.cv.CV_HAAR_SCALE_IMAGE,(20,20))

	if len(rects) == 0:
		return False

	rects[:,2:] += rects[:,:2]

	#highlighting faces
	for x1,y1,x2,y2 in rects:
		cv2.rectangle(img,(x1,y1),(x2,y2),(127,255,0),2)
	cv2.imwrite("{0}/{1}-{2}".format(f_dir,pcap,file),img)

	return True
	
def assembler(pcap,p_dir,f_dir):
	images = 0
	faces = 0

	p = rdpcap(pcap)
	sessions = p.sessions()

	for session in sessions:
		payload=""
		for packet in sessions[session]:
			try:
				if packet[TCP].dport==80 or packet[TCP].sport==80:
					#re-assemble
					payload+=str(packet[TCP].payload)
			except:
				pass

		headers=http_headers(payload)
		
		if headers is None:
			continue

		image,image_type=get_image(headers,payload)

		if image is not None and image_type is not None:
			#save image
			file="{0}-image_facial_{1}.{2}".format(pcap,images,image_type)

			fd=open("{0}/{1}".format(p_dir,file),"wb")
			fd.write(image)
			fd.close()

			images+=1

			#face recognition
			try:
				result=face_recog("{0}/{1}".format(p_dir,file),file,f_dir,pcap)

				if result is True:
					faces += 1

			except:
				pass

	return images,faces

def main():
	parser = argparse.ArgumentParser(description = "Image finder, face recognition")
	parser.add_argument("-pd",action="store",dest="p_dir",help="pictures directory")
	parser.add_argument("-fd",action="store",dest="f_dir",help="face directory")
	parser.add_argument("-p",action="store",dest="pcap",help="pcap file")
	results = parser.parse_args()

	if results.p_dir is None or results.f_dir is None or results.pcap is None :
		parser.print_help()
		exit(0)

	p_dir=results.p_dir #picture directory
	f_dir=results.f_dir #faces directory
	pcap=results.pcap

	images,faces=assembler(pcap,p_dir,f_dir) #http assembler

	print("Got: {0} images".format(images))
	print("Found: {0} faces".format(faces))

if __name__ == '__main__':
	main()
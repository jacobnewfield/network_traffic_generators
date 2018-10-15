#!/usr/bin/python
import socket
import time
import random

# Variables
IPVPN = ""
PORT = 12346
BUF = b'x' * random.randint(600,1500)
BLOCKING = 0
SLEEP = False
SLEEPTIME = 0.001
PRINT = False
ENTER = False

# Main
if ENTER:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
	sock.setblocking(BLOCKING)
	sock.setsockopt(socket.SOL_IP, socket.IP_TTL, 4)
	sock.connect((IPVPN, PORT))
	while True:
		try:		
			sock.send(BUF)
			if SLEEP:
				time.sleep(SLEEPTIME)
		except socket.error, e:
			# don't print to keep pumping data
			if PRINT:
				print "Socket Error occurred: %s" % e
			pass
else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(BLOCKING)
        while True:
                try:
                        #sock.sendto(MESSAGE, (IPESLOCAL, PORT))
                        sock.sendto(BUF, (IPVPN, PORT))
                        if SLEEP:
                                time.sleep(SLEEPTIME)
                except socket.error, e:
                        # don't print to keep pumping data
                        if PRINT:
                                print "Socket Error occurred: %s" % e
                        pass

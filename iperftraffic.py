#!/usr/bin/python
import subprocess
import signal
import sys
import os
import time

# Variables
IPIPERF = ""
BW = '50M'
T = '30'
PRINT = True
IPERFPID = 0

# Functions
def sigterm_handler(signal, frame):
    killiperfpid()
    sys.exit(0)
def killiperfpid():
    os.kill(IPERFPID, signal.SIGTERM)
def runcommand( command ):
    "Run the command given in a subprocess"
    executecommand = subprocess.Popen(['%s' % command], shell=True,
        #stdout=subprocess.PIPE,
        #stderr=subprocess.PIPE,
        )
    IPERFPID = executecommand.pid
def main():
    command = './iperf3 -c %s -b %s -u -t %s' % (IPIPERF, BW, T)
    runcommand( command )

# Main
if __name__ == '__main__':
    main()
    signal.signal(signal.SIGTERM, sigterm_handler)
    #signal.pause()
    time.sleep(int(T)+1)
    print 'Data may still be pumping\nPress Enter to stop...'

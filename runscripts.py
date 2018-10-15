#!/usr/bin/python

import subprocess
import getpass
import time
import sys
import os
import signal

# Variables
NUMIFACE = 1
NUMVPN = 0
IPERF = False
IFACESCRIPT = 'ifacetraffic.py'
VPNSCRIPT = 'vpntraffic.py'
IPERFSCRIPT = 'iperftraffic.py'
PIDS = []
PASSWORD = ''
PASSWORDCHECK = True
CLEARLOGS = False
if "-c" in str(sys.argv):
    CLEARLOGS = True
if ("-h" in str(sys.argv)) or ("--help" in str(sys.argv).lower()):
    print """RUNSCRIPTS()

    NAME
        runscripts - start traffic generating scripts

    SYNOPSIS
        runscripts [ -ch ]

    DESCRIPTION
        Runscripts starts 0 to many instances of 2 python scripts designed to simulate a heavy udp network traffic load use case. One python script generates udp network traffic through the F5 vpn tunnel while the second python script generates udp network traffic directly to the physical interface. The intent of this program is to reproduce ENOBUFS error messages (SYSCALL 55) on the F5 vpn tunnel when F5 vpn tunnel is running in DTLS tunnel type mode.

    OPTIONS
        -c  Clear F5 log files under ~/Library/Logs/F5networks and quit program. Helpful to capture logs that only pertain to the next program run.

        -h
        --help  Print this help information and exit"""
    quit()

# Get sudo password for commands requiring elevation rights
if PASSWORDCHECK == '':
	# Get and confirm password works
	FAIL = True
	print "Enter your password"
	for x in range(3):
        	PASSWORD = getpass.getpass()
        	checkpass = subprocess.check_output('sudo -k && echo \'%s\' | sudo -S ls 2>&1 | awk \'{if ($3 ~ /incorrect/) print $3}\'' % PASSWORD, shell=True).strip()
        	if checkpass == "incorrect":
                	print "Password incorrect"
        	else:
                	FAIL = False
                	break
	if FAIL:
        	print "Password incorrect\nPassword attempts exceeded\nCheck your password and try again later"
        	quit(1)

# Functions
def runcommand( command ):
    "Run the command given in a subprocess"
    executecommand = subprocess.Popen(['%s' % command], shell=True,
        #stdout=subprocess.PIPE,
        #stderr=subprocess.PIPE,
        )
    PIDS.append(executecommand.pid)
def exit():
    for pid in PIDS:
        os.kill(pid, signal.SIGTERM)
    sys.exit(0)
# Main
if CLEARLOGS:
    command = 'rm -f ~/Library/Logs/F5Networks/*.log'
    runcommand( command )
    print "F5 logs cleared"
    time.sleep(1)
    exit()
print 'Ramping up connections...'
if IPERF:
    command = 'python %s' % IPERFSCRIPT
    runcommand( command )
if NUMVPN:
    #time.sleep(5)
    command = 'python %s' % VPNSCRIPT
    runcommand( command )
if NUMIFACE:
   # time.sleep(10)
    command = 'python %s' % IFACESCRIPT
    for _ in range(NUMIFACE):
	runcommand( command )
	time.sleep(0.5)
response = raw_input("Running %s instance of %s and %s instances of %s\nPress Enter to stop..." % (NUMVPN, VPNSCRIPT, NUMIFACE, IFACESCRIPT))
exit()

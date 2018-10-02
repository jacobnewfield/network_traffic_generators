#!/usr/bin/python

import subprocess
import getpass
import time
import sys

# Variables
NUMIFACE = 10
NUMVPN = 1
IFACESCRIPT = 'ifacetraffic.py'
VPNSCRIPT = 'vpntraffic.py'
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
if PASSWORDCHECK:
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
def exit():
    command = "echo %s | sudo -S printf 'Stopping script instances...\n' | for pid in $(ps axc|awk '{if ($5==\"python\") print $1}'); do sudo kill -9 $pid; done;" % PASSWORD
    runcommand( command ) 
    quit(1)
# Main
if CLEARLOGS:
    command = 'rm -f ~/Library/Logs/F5Networks/*.log'
    runcommand( command )
    print "F5 logs cleared"
    exit()
print 'Ramping up connections...'
if NUMVPN:
    command = 'python %s' % VPNSCRIPT
    runcommand( command )
    time.sleep(1)
if NUMIFACE:
    command = 'python %s' % IFACESCRIPT
    for _ in range(NUMIFACE):
	runcommand( command )
	time.sleep(0.5)
response = raw_input("Running %s instance of %s and %s instances of %s\nPress Enter to stop..." % (NUMVPN, VPNSCRIPT, NUMIFACE, IFACESCRIPT))
exit()

#!/usr/bin/python

import subprocess
import getpass
import time

# Variables
NUMIFACE = 1
NUMVPN = 1
IFACESCRIPT = 'ifacetraffic.py'
VPNSCRIPT = 'vpntraffic.py'
PASSWORD = ''
PASSWORDCHECK = True
CLEARLOGS = False

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

# Main
if CLEARLOGS:
    command = 'rm -f ~/Library/Logs/F5Networks/*.log'
    runcommand( command )
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

command = "echo %s | sudo -S printf 'Stopping script instances...\n' | for pid in $(ps axc|awk '{if ($5==\"python\") print $1}'); do sudo kill -9 $pid; done;" % PASSWORD
runcommand( command )

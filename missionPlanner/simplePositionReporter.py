__author__ = 'Sven'

import sys
import clr
import time
import MissionPlanner #import *
clr.AddReference("MissionPlanner.Utilities") # includes the Utilities class
time.sleep(10)                                             # wait 10 seconds before starting
print 'Starting Mission'

#currentMode = cs.mode
#print currentMode
#if (currentMode == "Stabilize"):
	#MAV.setMode(RETURN_TO_LAUNCH)
#	Script.ChangeMode("RTL")                                      # Return to Launch point
#	print 'Returning to Launch'


while True:
    long=float(Script.GetParam("lng"))
    lat=float(Script.GetParam("lat"))
    alt=float(Script.GetParam("alt"))

    print "Long: "+str(long)+" Lat: "+str(lat)+" alt: "+str(alt)

    long=float(cs.lng)
    lat=float(cs.lat)
    alt=float(cs.alt)

    print "Long: "+str(long)+" Lat: "+str(lat)+" alt: "+str(alt)

    time.sleep(1)
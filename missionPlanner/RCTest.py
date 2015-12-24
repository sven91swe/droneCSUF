import sys
import clr
import time
import MissionPlanner #import *
clr.AddReference("MissionPlanner.Utilities") # includes the Utilities class
time.sleep(10)  

currentMode = cs.mode

while 1==1:
	print "Starting override Channel 4"
	Script.SendRC(4,2000,True)
	time.sleep(5)

	print "Stopping override"
	Script.SendRC(4,0,True)
	time.sleep(5)

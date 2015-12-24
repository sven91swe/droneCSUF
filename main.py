__author__ = 'Sven'
import network
import control
import time
import output
import display

screenBuffer=display.ScreenBuffer()
networkObject=network.Network(screenBuffer)

#Sleep so that networkObject might fetch initial data.
time.sleep(2)

behaviorObject=control.SimpleTestBehavior(networkObject)
#outputObject=output.outputOfDroneState(networkObject)

display.Display(screenBuffer)
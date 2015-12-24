__author__ = 'Sven'
import threading
import time
import network
import support


class outputOfDroneState(threading.Thread):
    def __init__(self, n):
        threading.Thread.__init__(self)
        self.network=n

        self.start()

    def run(self):
        while True:
            currentState=self.network.getCurrentState()
            print("\nThe UAVs current parameters")
            print("Mode: "+str(currentState.mode))
            print("Position: "+str(currentState.getPosition()))
            #print("Attitude: "+str(currentState.getAttitude()))
            #print("Velocity: "+str(currentState.getVelocity()))

            time.sleep(1)

class calcOfUpdateFrequency(threading.Thread):
    def __init__(self, n):
        threading.Thread.__init__(self)

        self.network=n
        self.lastDronestate=self.network.getCurrentState()

        self.runTest=True
        self.time=0

        self.start()

    def run(self):
        t1=time.clock()
        k=0
        while self.runTest:
            droneState=self.network.getCurrentState()
            if self.lastDronestate!=droneState:
                self.lastDronestate=droneState
                k=k+1
            time.sleep(0.005)
        t2=time.clock()

        self.time=t2-t1

        print("Time: "+str(self.time)+" --- Number of states: "+str(k))

class testOfUpdateFrequency(threading.Thread):
    def __init__(self, n):
        threading.Thread.__init__(self)
        self.testModule=calcOfUpdateFrequency(n)
        self.start()

    def run(self):
        time.sleep(120)
        self.testModule.runTest=False
__author__ = 'Sven'
import support
import threading
import time
import socket
import judgeCommunication


class Network:
    def __init__(self, screenbuffer):
        self.ioDrone = DroneCommunication(screenbuffer)
        self.ioJudge = judgeCommunication.JudgeCommunication(screenbuffer ,self.ioDrone)

    def getCurrentState(self):
        """

        :rtype : DroneState
        """
        return self.ioDrone.getGurrentState()

    def getObstacles(self):
        return self.ioJudge.getObstacles()

    def setWaypoint(self, w):
        self.ioDrone.setWaypoint(w)


class DroneCommunication(threading.Thread):
    def __init__(self, screenbuffer):
        threading.Thread.__init__(self)
        self.currentState = support.DroneState([0, 0, 0], [0, 0, 0], 0, 0, "Mode")
        self.nextWaypoint = support.Waypoint("StartValue", 0, [0, 0, 0], 0)
        self.currentWaypoint = self.nextWaypoint
        self.updateWaypoint = False

        self.screenbuffer=screenbuffer

        # Something about starting TCP communication
        self.messageCounter=1

        self.host = 'localhost'
        self.port = 50000
        self.size = 1024




        self.start()

        #Something about starting the thread that communicates with missionplanner.

    def run(self):
        while True:
            if self.updateWaypoint:
                self.currentWaypoint=self.nextWaypoint
                self.updateWaypoint=False

            messageToSend=support.MessageHandle.waypointToMessage(self.currentWaypoint)
            self.communicateWithMissionPlanner(messageToSend)

            time.sleep(0.01)

    def communicateWithMissionPlanner(self, messageToSend):

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host,0))

        try:
            self.s.send(messageToSend)
            returnMessage = self.s.recv(self.size)

            self.currentState=support.MessageHandle.messageToDroneState(returnMessage)
            self.screenbuffer.updatedAirplane(self)

        finally:
            self.s.close()

    def getCurrentState(self):
        return self.currentState

    def setWaypoint(self, w):
        self.nextWaypoint = w
        self.updateWaypoint = True
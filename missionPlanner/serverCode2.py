import SocketServer
import sys
import clr
import time
clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") # includes the Utilities class
import socket
import threading
import SocketServer

class MyUDPHandler(SocketServer.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        global dataH
        data = self.request[0].strip()
        socket = self.request[1]
        dataH.messageRecieved=str(data)
        socket.sendto(dataH.messageToSend, self.client_address)


class dataHandle(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.messageToSend=bytes("1;2.5;55;64;2;78;65;52;558;25;","utf-8")
        self.messageRecieved="0;0;0;0;0;0;"
        self.incomingData=[0,0,0,0,0,0]
        self.lastIncomingCounter=-1

        self.start()


    def decodeIncomingMessage(self):
        sData=self.messageRecieved.decode("utf-8")

        start=0
        data=[]

        while True:
            end=sData.find(";", start)
            if end==-1:
                break
            else:
                data.append(sData[start:end])
                start=end+1

        self.incomingData=data

    def actOnIncomingMessage(self):
        self.decodeIncomingMessage()

        if float(self.incomingData[0])!=float(self.lastIncomingCounter):

            acceptGuidedWaypoint=str(cs.mode)==str("Auto") or str(cs.mode)==str("Guided")

            if float(self.incomingData[1])==float(2) and acceptGuidedWaypoint:
                if str(cs.mode)==str("Auto"):
                    Script.ChangeMode("Guided")                     # changes mode to "Guided"

                self.lastIncomingCounter=float(self.incomingData[0])

                item = MissionPlanner.Utilities.Locationwp() # creating waypoint
                lat = float(self.incomingData[3])                                         # Latitude value
                lng = float(self.incomingData[4])                                         # Longitude value
                alt = float(self.incomingData[2])                                           # altitude value
                MissionPlanner.Utilities.Locationwp.lat.SetValue(item,lat)     # sets latitude
                MissionPlanner.Utilities.Locationwp.lng.SetValue(item,lng)   # sets longitude
                MissionPlanner.Utilities.Locationwp.alt.SetValue(item,alt)     # sets altitude
                #print 'WP '+str(self.incomingData[0])+' set'
                MAV.setGuidedModeWP(item)                                    # tells UAV "go to" the set lat/long @ alt

                print("New Waypoint received, #"+str(int(self.lastIncomingCounter)))
            elif float(self.incomingData[1])==float(1):
                Script.ChangeMode("Auto")

    def outgoingMessage(self):
        long=float(cs.lng)
        lat=float(cs.lat)
        alt=float(cs.alt)
        airspeed=float(cs.airspeed)
        heading=float(cs.groundcourse)
        roll=float(cs.roll)
        pitch=float(cs.pitch)
        yaw=float(cs.yaw)
        mode=str(cs.mode)

        modeMessage=mode+"1;"
        posMessage=str(alt)+";"+str(lat)+";"+str(long)+";"
        attitudeMessage=str(roll)+";"+str(pitch)+";"+str(yaw)+";"
        velocityMessage=str(airspeed)+";"
        headingMessage=str(heading)+";"

        messageToSend=modeMessage+posMessage+attitudeMessage+velocityMessage+headingMessage
        #messageToSend=bytes(messageToSend,"utf-8")
        self.messageToSend=messageToSend

    def run(self):
        while True:
            self.actOnIncomingMessage()
            self.outgoingMessage()

            time.sleep(0.01)
print "Starting the server: Do not start the client until the server has been started"
time.sleep(2)

HOST="localhost"
PORT=49500
dataH=dataHandle()
server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
print "The server has started"
server.serve_forever()



print "You may now start the client"

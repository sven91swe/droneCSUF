import SocketServer
import sys
import clr
import time
clr.AddReference("MissionPlanner")
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities") # includes the Utilities class
import socket
import threading
print "Starting the server: Do not start the client until the server has been started"
time.sleep(2)


class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.host = ''
        self.port = 50000
        self.backlog = 5 
        self.size = 1024
        print "Before socket"
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host,self.port))
        self.s.listen(self.backlog)
        print "After socket"
        self.messageToSend=bytes("1;2.5;55;64;2;78;65;52;558;25;","utf-8")
        self.messageRecieved="0;0;0;0;0;0;"
        self.hasRecievedMessage=False
        self.runMore=True
        self.start()
    def run(self):   
        while self.runMore: 
            client, address = self.s.accept() 
            self.messageRecieved = client.recv(self.size)
            #print "Recieved:  "+self.messageRecieved.decode("utf-8")
            if self.messageRecieved:
                client.send(buffer(self.messageToSend))
                self.hasRecievedMessage=True
            client.close()
        self.s.close()

class dataHandle(threading.Thread):
    def __init__(self,s):
        threading.Thread.__init__(self)
        self.incomingData=[0,0,0,0,0,0]
        self.lastIncomingCounter=-1
        self.server=s

        self.start()


    def decodeIncomingMessage(self):
        sData=self.server.messageRecieved.decode("utf-8")

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
                else:
                    print "Did not change mode due to already being in "+str(cs.mode)

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
            else:
                print("Did not change mode due to already being in "+str(cs.mode))

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

        modeMessage=mode+";"
        posMessage=str(alt)+";"+str(lat)+";"+str(long)+";"
        attitudeMessage=str(roll)+";"+str(pitch)+";"+str(yaw)+";"
        velocityMessage=str(airspeed)+";"
        headingMessage=str(heading)+";"

        messageToSend=bytes(modeMessage+posMessage+attitudeMessage+velocityMessage+headingMessage,"utf-8")
        self.server.messageToSend=messageToSend

    def run(self):
        while True:
            self.actOnIncomingMessage()
            self.outgoingMessage()

            time.sleep(0.01)

serv=Server()
time.sleep(2)
dataH=dataHandle(serv)

print "The server has started"
print "You may now start the client"
__author__ = 'Sven'

import threading
import time
import requests
import json
import random
import settings
import support



class JudgeCommunication():
    def __init__(self, screenbuffer, droneCommunication):
        self.session=requests.session()
        self.lastLogin=-500
        k=settings.numberOfThreadsForInteroperability
        self.login()
        self.screenbuffer=screenbuffer
        self.droneCommunication=droneCommunication

        self.serverInformation=ServerInformation(self.session,k,self,screenbuffer) #add reference to screenbuffer
        self.obstacleInformation=ObstacleInformation(self.session,k,self, screenbuffer) #add reference to screenbuffer
        self.uasTelemetry=UASTelemetry(self.session,k, self, droneCommunication) #Add reference to droneCommunication


    def serverAddress(self):
        return settings.judgeServerAddress

    def login(self):
        if time.clock()-self.lastLogin>5:
            payload = {'username': 'csuf', 'password': 'test'}
            r = self.session.post(self.serverAddress()+"/api/login", data=payload)

            self.lastLogin=time.clock()

            if r.status_code==requests.codes.ok:
                print("Successful login")

    def getObstacleInformation(self):
        return self.obstacleInformation.getCurrentObstacleInformation()


class UASTelemetry(threading.Thread):
    def __init__(self,s,k,p, dronecommunication):
        threading.Thread.__init__(self)

        self.parent=p
        self.workers=[0]*k

        self.droneCommunication=dronecommunication

        for i in range(k):
            self.workers[i]=UASTelemetryWorker(s, self)

        self.k=k

        print("uasTelemetry created")
        self.start()

    def run(self):
        i=0
        while True:
            lat=random.random()
            long=random.random()
            alt=random.random()+200
            heading=random.random()*350

            while not self.workers[i].request(lat ,long, alt, heading):
                i=i+1

                if i==self.k:
                    i=0



            time.sleep(0.1)

    def login(self):
        self.parent.login()

    def serverAddress(self):
        return self.parent.serverAddress()

class UASTelemetryWorker(threading.Thread):
    def __init__(self,s,p):
        threading.Thread.__init__(self)

        self.ready=True
        self.session=s
        self.parent=p

        self.payload=0

        self.start()

    def run(self):
        while True:
            if not self.ready:
                try:
                    r=self.session.post(self.parent.serverAddress()+"/api/interop/uas_telemetry", data=self.payload, timeout=settings.timeToTimeOut)
                    if r.status_code==requests.codes.ok:
                        #print(r.status_code)
                        pass
                    else:
                        self.parent.login()
                except Exception:
                    pass

            self.ready=True
            time.sleep(0.01)

    def request(self,lat, long, alt, heading):
        if self.ready:
            self.payload={'latitude':str(lat), 'longitude':  str(long), 'altitude_msl': str(alt), 'uas_heading': str(heading)}
            self.ready=False

            return True

        else:
            return False

class ObstacleInformation(threading.Thread):
    def __init__(self,s,k,p, screenbuffer):
        threading.Thread.__init__(self)

        self.parent=p
        self.workers=[0]*k

        self.screenbuffer=screenbuffer
        self.currentObstacleData=support.Obstacles()

        for i in range(k):
            self.workers[i]=ObstacleInformationWorker(s, self)

        self.counter=1
        self.lastCounterReceived=0
        self.k=k

        print("obstacleInformation created")
        self.start()

    def run(self):
        i=0
        while True:


            while not self.workers[i].request(self.counter):
                i=i+1

                if i==self.k:
                    i=0

            self.counter=self.counter+1


            time.sleep(0.1)


    def login(self):
        self.parent.login()

    def data(self,data,c):
        if c>self.lastCounterReceived:
            self.lastCounterReceived=c
            #print("Obstacle \t"+str(c))
            #print("ServerTime: "+str(data['moving_obstacles'])+" \t "+str(c))

            #Use support and update self.currentObstacleData

    def serverAddress(self):
        return self.parent.serverAddress()

    def getCurrentObstacleInformation(self):
        return self.currentObstacleData


class ObstacleInformationWorker(threading.Thread):
    def __init__(self,s,p):
        threading.Thread.__init__(self)

        self.ready=True
        self.session=s
        self.parent=p
        self.counter=0

        self.start()

    def run(self):
        while True:
            if not self.ready:
                try:
                    r=self.session.get(self.parent.serverAddress()+"/api/interop/obstacles", timeout=settings.timeToTimeOut)
                    if r.status_code==requests.codes.ok:
                        j=json.loads(r.text)

                        self.parent.data(j,self.counter)



                    else:
                        self.parent.login()
                except Exception:
                    pass

            self.ready=True
            time.sleep(0.01)

    def request(self,c):
        if self.ready:
            self.counter=c
            self.ready=False

            return True

        else:
            return False

class ServerInformation(threading.Thread):
    def __init__(self,s,k,p, screenbuffer):
        threading.Thread.__init__(self)

        self.parent=p
        self.workers=[0]*k

        for i in range(k):
            self.workers[i]=ServerInformationWorker(s, self)

        self.screenbuffer=screenbuffer

        self.counter=1
        self.lastCounterReceived=0
        self.k=k

        print("serverInformation created")
        self.start()

    def run(self):
        i=0
        while True:


            while not self.workers[i].request(self.counter):
                i=i+1

                if i==self.k:
                    i=0

            self.counter=self.counter+1


            time.sleep(0.1)


    def login(self):
        self.parent.login()

    def data(self,data,c):
        if c>self.lastCounterReceived:
            self.lastCounterReceived=c
            #print("ServerTime: "+data['server_time']+" \t "+str(c))


            self.screenbuffer.serverMessage(data['server_time'],data['server_info']['message_timestamp'],data['server_info']['message'])


    def serverAddress(self):
        return self.parent.serverAddress()

class ServerInformationWorker(threading.Thread):
    def __init__(self,s,p):
        threading.Thread.__init__(self)

        self.ready=True
        self.session=s
        self.parent=p
        self.counter=0

        self.start()

    def run(self):
        while True:
            if not self.ready:
                try:
                    r=self.session.get(self.parent.serverAddress()+"/api/interop/server_info", timeout=settings.timeToTimeOut)
                    if r.status_code==requests.codes.ok:
                        j=json.loads(r.text)

                        self.parent.data(j,self.counter)



                    else:
                        self.parent.login()
                except Exception:
                    pass

            self.ready=True
            time.sleep(0.01)

    def request(self,c):
        if self.ready:
            self.counter=c
            self.ready=False

            return True

        else:
            return False


#JudgeCommunication(None, None)
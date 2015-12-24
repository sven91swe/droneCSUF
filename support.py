__author__ = 'Sven'

import math

class DroneState:
    def __init__(self, p, a, v, h, m):
        """

        :rtype : DroneState
        """

        #mode: 1 - auto, 2 - guided, 3 - return to home
        self.mode=m
        self.position=p
        self.attitude=a
        self.velocity=v
        self.heading=h
        self.point=Point(p[2],p[1],p[0])
    def getPoint(self):
        return self.point
    def getVelocity(self):
        return self.velocity
    def getAttitude(self):
        return self.attitude
    def getPosition(self):
        return self.position

class Obstacles:
    def __init__(self):
        self.stationary=[]
        self.moving=[]
    def addStationaryObstacle(self, o):
        self.stationary.append(o)
    def addMovingObstacle(self,o):
        self.moving.append(o)

class StationaryObstacle:
    def __init__(self, p, d,k,i):
        #Counter for the request
        self.k=k
        #Obstacle number #
        self.i=i
        #position is a vector [lat, long]
        self.position=p
        #dimension is a vector [height, radious] both in feet
        self.dimension=d
    def getPosistion(self):
        return self.position
    def getDimension(self):
        return self.dimension

class MovingObstacle:
    def __init__(self,p, d,k,i):
        #Counter for the request
        self.k=k
        #Obstacle number #
        self.i=i
        #position is a vector [lat, long]
        self.position=p
        #dimension is a vector [alt, radious] both in feet
        self.dimension=d
    def getPosition(self):
        return self.position
    def getDimension(self):
        return self.dimension

class MovingObstacleSpeed:
    def __init__(self,i):
        self.i=i
        self.savedPositions=10
        self.list=[MovingObstacle([0,0],[0,0],-1,self.i)]*self.savedPositions
        v=[0]*self.savedPositions
        self.k=0
        self.averageSpeed=0
    def addObstacleTimeStep(self,o):
        if o.i==self.i:
            if self.k==self.savedPositions-1:
                self.k=0
            else:
                self.k=self.k+1

            self.list[self.k]=o

            if self.k==self.savedPositions-1:
                self.v[self.k]=self.speedBetweenStates(list[self.k],list[0])

            ##Continue here to check for time...





    def speedBetweenStates(self,o1,o2):
        pass


class Waypoint:
    def __init__(self, s, prio, pos, mode):
        """
        :rtype : Waypoint
        """
        self.source = s
        self.priority = prio
        #position [altitude, lat, long]
        self.position = pos
        #should be 2 for guided
        self.mode=mode
        self.drop=0
        self.point=Point(pos[2],pos[1],pos[0])


class MessageHandle:
    #Variables for outgoing message / waypoint
    outgoingMessageCounter=1
    currentOutgoingWaypoint=Waypoint("StartValue", 0, [0, 0, 0], 0)
    currentOutgoingMessage=bytes("start","utf-8")

    #Variables for incoming message / droneState
    currentDroneState=DroneState([0, 0, 0], [0, 0, 0], 0,0, "Mode")

    def getListFromCommaSeparatedString(sData):
        start=0
        data=[]

        while True:
            end=sData.find(";", start)
            if end==-1:
                break
            else:
                data.append(sData[start:end])
                start=end+1
                #print(data)

        return data
    def changeListFromStringToFloat(dList):
        data=[]

        data.append(dList[0])

        for k in range(1,len(dList)):
            number=dList[k]
            data.append(float(number))

        return data

    def messageToDroneState(bString):
        #Expeting dString in the format
        #mode(numerical value); pos(3 values); attitude(3 values); velocity(3 values);
        #mode: 1 - auto, 2 - guided, 3 - return to home

        dString=bString.decode("utf-8")
        d=MessageHandle.getListFromCommaSeparatedString(dString)
        listOfFloat=MessageHandle.changeListFromStringToFloat(d)

        mode=listOfFloat[0]
        pos=listOfFloat[1:4]
        att=listOfFloat[4:7]
        v=listOfFloat[7]
        h=listOfFloat[8]

        notSameMode=mode!=MessageHandle.currentDroneState.mode
        notSamePos=pos!=MessageHandle.currentDroneState.position
        notSameAtt=att!=MessageHandle.currentDroneState.attitude
        notSameV=v!=MessageHandle.currentDroneState.velocity
        notSameH=h!=MessageHandle.currentDroneState.heading

        if notSameMode or notSamePos or notSameAtt or notSameV or notSameH:
            MessageHandle.currentDroneState=DroneState(pos, att, v, h, mode)

        return MessageHandle.currentDroneState

    def waypointToMessage(w):
        #message will be in the form:
        #number; mode; altitude; long; lat; drop
        #mode: 1 - auto, 2 - guided, 3 - return to home
        #drop: 0 - do not drop, 1 - drop
        if w!=MessageHandle.currentOutgoingWaypoint:
            MessageHandle.currentOutgoingMessage=bytes(str(MessageHandle.outgoingMessageCounter)+";"+str(w.mode)+";"+str(w.position[0])+";"+str(w.position[1])+";"+str(w.position[2])+";"+str(w.drop)+";", "utf-8")

            #print(str(MessageHandle.outgoingMessageCounter))

            MessageHandle.outgoingMessageCounter=MessageHandle.outgoingMessageCounter+1
            MessageHandle.currentOutgoingWaypoint=w

            if MessageHandle.outgoingMessageCounter>995:
                MessageHandle.outgoingMessageCounter=1

        return MessageHandle.currentOutgoingMessage

class Point:
    def __init__(self, long, lat, alt):
        self.long=long
        self.lat=lat
        self.alt=alt
    def distanceBetweenPoints3D(p1,p2):

        s = Point.vectorBetweenPoints(p1.long,p1.lat,p1.alt,p2.long,p2.lat,p2.alt)

        return math.sqrt(math.pow(s[0],2)+math.pow(s[1],2)++math.pow(s[2],2))

    def distanceBetweenPoints2D(p1,p2):

        s = Point.vectorBetweenPoints(p1.long,p1.lat,p1.alt,p2.long,p2.lat,p2.alt)

        return math.sqrt(math.pow(s[0],2)+math.pow(s[1],2))

    def vectorBetweenPoints(long1,lat1,alt1,long2,lat2,alt2):
        s=[0]*3
        averageLat=(lat1+lat2)/2
        averageLong=(long1+long2)/2
        s[0]=Point.internalDistanceBetweenPoints2D(long1,averageLat,long2,averageLat)
        s[1]=Point.internalDistanceBetweenPoints2D(averageLong,lat1,averageLong,lat2)
        s[2]=alt1-alt2

        return s

    def internalDistanceBetweenPoints2D(long1,lat1,long2,lat2):
        long1=long1/360*2*math.pi
        long2=long2/360*2*math.pi
        lat1=lat1/360*2*math.pi
        lat2=lat2/360*2*math.pi

        deltaLong=long1-long2
        deltaLat=lat1-lat2

        #radius 6317km
        radius=6371 * 0.621371192 * 5280

        a=math.pow(math.sin(deltaLat/2),2)+math.cos(lat1)*math.cos(lat2)*math.pow(math.sin(deltaLong/2),2)
        c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))

        return radius*c

def selfTest():
      s1=Point.internalDistanceBetweenPoints2D(-77.037879,38.898556,-77.037895,38.896392)

      p1=Point(-77.037879,38.898556,50)
      p2=Point(-77.037895,38.896392,50)
      p3=Point(-77.037879,38.898556,150)

      s2=Point.distanceBetweenPoints3D(p1,p2)
      s3=Point.distanceBetweenPoints3D(p1,p3)
      print("Distance should be approximatly 782.27, it is:"+str(s1))
      print("Distance should be approximatly 782.27, it is:"+str(s2))
      print("Distance should be approximatly 100, it is:"+str(s3))


#selfTest()
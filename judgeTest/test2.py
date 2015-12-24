__author__ = 'Sven'

import requests
import json
import time

s=requests.session()


serverAdress="http://192.168.27.1"
#Log on to server
#payload = {'username': 'csuf', 'password': 'test'}
payload = {'username': 'csuf', 'password': 'test'}
r = s.post(serverAdress+"/api/login", data=payload)
print(r.status_code)
#print(r.text)
#print(r.headers)






#Request server message + time, 50 times. 10 times a second.
t1=time.clock()
timeperiod=0.1
for i in range(600):

    t=time.clock()
    r=s.get(serverAdress+"/api/interop/obstacles")
    print(" \n"+str(r.status_code))
    #print(str(r.headers))
    #print(r.request.headers)
    #print(r.elapsed)

    j=json.loads(r.text)
    print(j)
    print(j['stationary_obstacles'][0]['longitude'])
    print(len(j['stationary_obstacles']))

    #print("Message: "+j['server_info']['message'])
    #print("Message Timestamp: "+j['server_info']['message_timestamp'])
    #print("ServerTime: "+j['server_time'])
    timeToSleep=max(timeperiod-(time.clock()-t),0)
    print(str(time.clock()-t))
    print(timeToSleep)
    time.sleep(timeToSleep)

print(time.clock()-t1)

#Use for sleep when difference is negative.

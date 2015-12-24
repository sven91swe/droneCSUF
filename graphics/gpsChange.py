__author__ = 'Sven'

import math

dLat=38.1508
dLong=-76.42940556


dLong=max(dLong, -dLong)

Long=math.floor(dLong)
Lat=math.floor(dLat)

diffLong=dLong-Long
diffLat=dLat-Lat

mLong=math.floor(diffLong*60)
mLat=math.floor(diffLat*60)

diffLong=dLong-Long-mLong/60
diffLat=dLat-Lat-mLat/60

sLong=diffLong*60*60
sLat=diffLat*60*60

sLong=math.floor(sLong*1000)/1000
sLat=math.floor(sLat*1000)/1000

print("LONG: W"+str(Long)+" M"+str(mLong)+" S"+str(sLong))
print("LAT: N"+str(Lat)+" M"+str(mLat)+" S"+str(sLat))
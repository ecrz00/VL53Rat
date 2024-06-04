from machine import  I2C, Timer, Pin
from VL53Rat import VL53Rat
from time import sleep
import time

bottomEnd, topEnd = [], []
timep, limit = 10, 15
info = None

def getTime():
		tup = time.localtime()
		fecha = str(tup[0]) + '/' + str(tup[1]) + '/' + str(tup[2])
		hora  = str(tup[3]) + ':' + str(tup[4]) + ':' + str(tup[5])
		tiempo = [fecha, hora]
		return tiempo
	
def getInfo(signal):
	global info, bottomEnd, topEnd
	topEnd = getTime()
	info = sensorUno.returnInfo()
	print(info + ' between '+str(bottomEnd[0])+ ' at '+str(bottomEnd[1])+ ' and '+str(topEnd[0])+ ' at ' +str(topEnd[1]))
	bottomEnd = topEnd

signal = Timer()
I2C_bus = I2C(1, sda=Pin(2), scl = Pin(3), freq=400000)
sensorUno = VL53Rat(I2C_bus, 0x30, 28, limit, 1)
sensorDos = VL53Rat(I2C_bus, 0x30, 29, limit, 2)

if __name__ == '__main__':
	signal.init(period=timep*1000, mode=Timer.PERIODIC, callback=getInfo)
	bottomEnd= getTime()
	sensorUno.init()
	
	while True:
		sensorUno.getDistance()
		sleep(1)
	




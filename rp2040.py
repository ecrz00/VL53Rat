from machine import  I2C, Timer, Pin, UART
from VL53Rat import VL53Rat
from time import sleep
from utime import sleep_ms
import time

bottomEnd, topEnd = [], []
timep, limit = 10, 15
info = None
data2send = []

pin_tx = Pin(0, Pin.OUT)
pin_rx = Pin(1, Pin.IN)

def getTime():
		tup = time.localtime()
		fecha = str(tup[0]) + '/' + str(tup[1]) + '/' + str(tup[2])
		hora  = str(tup[3]) + ':' + str(tup[4]) + ':' + str(tup[5])
		tiempo = [fecha, hora]
		return tiempo
#end def

def getInfo(signal):
	global info, bottomEnd, topEnd, data2send
	topEnd = getTime()
	rat1, rat2 = sensorUno.returnInfo(), sensorDos.returnInfo()
	data2send = f'{bottomEnd[0]}, {bottomEnd[1]}, {topEnd[0]}, {topEnd[1]}, {rat1}, {rat2}'
	uart.write(data2send)
	bottomEnd = topEnd
#end def

signal = Timer()
I2C_bus = I2C(1, sda=Pin(2), scl = Pin(3), freq=400000)
uart   = UART(0, baudrate=115200, tx=pin_tx, rx=pin_rx, timeout=1, timeout_char=1)
sensorUno = VL53Rat(I2C_bus, 0x30, 28, limit, 1)
sensorDos = VL53Rat(I2C_bus, 0x31, 29, limit, 2)

def main():
	global bottomEnd
	signal.init(period=timep*1000, mode=Timer.PERIODIC, callback=getInfo)
	bottomEnd = getTime()
	sensorUno.init()
	sensorDos.init()
	while True:
		sensorUno.getDistance()
		sensorDos.getDistance()
		#print('\n')
		sleep(1)
#end def

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print('--- Caught Exception ---')
		import sys
		sys.print_exception(e)
		print('----------------------------')
	





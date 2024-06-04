from VL53L0X import VL53L0X
from machine import Pin, I2C, Timer
from utime import sleep_ms

class VL53Rat:
	def __init__(self, i2c, address, pin, limit, numSen):
		self.numSen = numSen
		self.vl53l0x = None
		self.address = address
		self.i2c = i2c
		self.xshut = Pin(Pin(pin, Pin.OUT, value = 0))
		self.timer = Timer()
		self.miliseg = 0
		self.seg = 0
		self.min = 0
		self.distance = 0
		self.hrs = 0
		self.ind = None
		self.limit = limit
		
	def getTime(self):
		tup = time.localtime()
		fecha = str(tup[0]) + '/' + str(tup[1]) + '/' + str(tup[2])
		hora  = str(tup[3]) + ':' + str(tup[4]) + ':' + str(tup[5])
		tiempo = [fecha, hora]
		return tiempo
	
	def init(self):
		self.xshut.value(1)
		sleep_ms(2)
		self.vl53l0x = VL53L0X(self.i2c,self.adddress)
	
	def counter(self, self.timer):
		self.miliseg += 1
		if(self.miliseg == 1000):
			self.seg += 1
			self.miliseg = 0
			if(self.seg == 60):
				self.min += 1
				self.seg = 0
				if (self.min == 60):
					self.hrs += 1
					self.minu = 0
		
	def getDistance(self):
		self.vl53l0x.start()
		self.distance = self.vl53l0x.read()
		self.vl53l0x.stop()
		if self.distance < self.limit*10 and self.ind != 'menor':
			self.timer.init(freq = 1000, mode = Timer.PERIODIC, callback = self.counter())
			self.ind = 'menor'
		elif self.distance >= self.lim*10 and self.ind != 'mayor':
			self.timer.deinit()
			self.ind = 'mayor'
	
	def returnInfo(self):
		self.TopEnd = self.getTime()
		info = 'Sensor ' +str(self.numSen)+ ' detected presence for '+str(self.hrs)+' : '+str(self.min)+' : '+str(self.seg)+' :'+str(self.miliseg)
		self. miliseg, self.seg, self.min, self.hrs = 0, 0, 0, 0
		return info

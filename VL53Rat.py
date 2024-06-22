from machine import Pin, Timer
from utime import sleep_ms

class VL53Rat:
	def __init__(self, limit):
		self.timer = Timer()
		self.miliseg = 0
		self.seg = 0
		self.min = 0
		self.hrs = 0
		self.limit = limit
		self.ind = None
		#self.pin = Pin(pin,Pin.OUT,value=0)
	#end def
	
	def counter(self, timer):
		self.miliseg += 1
		if(self.miliseg == 1000):
			self.seg += 1
			self.miliseg = 0
			if(self.seg == 60):
				self.min += 1
				self.seg = 0
				if (self.min == 60):
					self.hrs += 1
					self.min = 0
	#end def
	
	def checkDistance(self, distance):
		if distance < self.limit and self.ind != 'menor':
			self.timer.init(freq = 1000, mode = Timer.PERIODIC, callback = self.counter)
			#print('hay presencia: '+str(distance))
			#self.pin.value(1)
			self.ind = 'menor'
		elif distance >= self.limit and self.ind != 'mayor':
			self.timer.deinit()
			#self.pin.value(0)
			#print('no hay presencia: '+str(distance))
			self.ind = 'mayor'
	#end def
	
	def returnInfo(self):
		info = f'{str(self.hrs)}:{str(self.min)}:{str(self.seg)}:{str(self.miliseg)}'
		self.miliseg, self.seg, self.min, self.hrs = 0, 0, 0, 0
		return info
	#end def




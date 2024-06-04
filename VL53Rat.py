from VL53L0X import VL53L0X
from machine import Pin, Timer
from utime import sleep_ms

class VL53Rat:
	def __init__(self, i2c, address, pin, limit, numSen):
		self.numSen = numSen
		self.i2c = i2c
		self.address = address
		self.timer = Timer()
		self.miliseg = 0
		self.seg = 0
		self.min = 0
		self.distance = 0
		self.hrs = 0
		self.ind = None
		self.limit = limit
		self.xshut = Pin(pin, Pin.OUT, value = 0)
		self.sensor = None
	#end def
	
	def init(self):
		self.xshut.value(1)
		sleep_ms(1)
		self.sensor = VL53L0X(self.i2c, self.address)
		"""try:
			self.sensor = VL53L0X(self.i2c, self.address)
		except Exception as e:
			print("Error initializing VL53L0X sensor:", e)"""
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
	
	def getDistance(self):
		self.sensor.start()
		self.distance = self.sensor.read()
		self.sensor.stop()
		#print(self.distance)
		if self.distance < (self.limit*10) and self.ind != 'menor':
			self.timer.init(freq = 1000, mode = Timer.PERIODIC, callback = self.counter)
			#print('hay presencia: '+str(self.distance))
			self.ind = 'menor'
		elif self.distance >= (self.limit*10) and self.ind != 'mayor':
			self.timer.deinit()
			#print('no hay presencia: '+str(self.distance))
			self.ind = 'mayor'
	#end def
	
	def returnInfo(self):
		info = f'{str(self.hrs)}:{str(self.min)}:{str(self.seg)}:{str(self.miliseg)}'
		self.miliseg, self.seg, self.min, self.hrs = 0, 0, 0, 0
		return info
	#end def


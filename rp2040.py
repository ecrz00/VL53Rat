from machine import  I2C, Timer, Pin, SPI
from VL53Rat import VL53Rat
from VL53L0X import VL53L0X
import uos
from sdcard import SDCard
from neopixel import NeoPixel
import time

numSen, timep, limit = 2, 600, 150

#rat = None #[None]*numSen
bottomEnd, topEnd = '', ''

TCA_addr = 0x70
TCA_dir = [b'\0x01',b'\0x02', b'\0x04', b'\0x08', b'\0x10', b'\0x20', b'\0x40', b'\0x80']
#pines = [10,15]

signal = Timer()

I2C_bus = None
SPI_bus = None

NeoP = Pin(17, Pin.OUT, value = 1)
NeoD = NeoPixel(Pin(16), 1)

sensor = [None]*numSen
vl53 = [None]*numSen

rst = Pin(26, Pin.OUT)
xshut = [Pin(29, Pin.OUT), Pin(28, Pin.OUT)]

def hsv2rgb(h, s, v):
	if (s < 0) or (v < 0) or (h > 360) or (s > 1) or (v > 1):
		return False
	C = s * v
	X = C * (1 - abs(h / 60.0 % 2 - 1))
	m = v - C
	if h < 60:
		R, G, B = C, X, 0
	elif h < 120:
		R, G, B = X, C, 0
	elif h < 180:
		R, G, B = 0, C, X
	elif h < 240:
		R, G, B = 0, X, C
	elif h < 300:
		R, G, B = X, 0, C
	else:
		R, G, B = C, 0, X
	return int((R + m) * 255), int((G + m) * 255), int((B + m) * 255)
#end def

def getTime():
		tup = time.localtime()
		fecha = str(tup[0]) + '/' + str(tup[1]) + '/' + str(tup[2])
		hora  = str(tup[3]) + ':' + str(tup[4]) + ':' + str(tup[5])
		tiempo = f'{fecha},{hora}'
		return tiempo
#end def

def rstHardware():
	global rst, xshut
	rst.value(0)
	for i in range(numSen):
		xshut[i].value(0)
	time.sleep(1)
	rst.value(1)
	for i in range(numSen):
		xshut[i].value(1)
#end def

def setupSD(spi,cs):
	sd = SDCard(spi, cs)
	# Mount filesystem
	vfs = uos.VfsFat(sd)
	uos.mount(vfs, "/sd")
	try:
		open("/sd/ratitas.txt", "x")
	except:
		pass
#end def

def setupSPI():
	global SPI_bus
	pin_mosi = Pin(19)
	pin_miso = Pin(20)
	pin_sck = Pin(18)
	pin_cs = Pin(21, Pin.OUT, value=1) # Assign chip select (CS) pin (and start it high)
	SPI_bus = SPI(0, baudrate=1000000, polarity=0, phase=0,bits=8, firstbit=SPI.MSB, sck = pin_sck, mosi=pin_mosi, miso = pin_miso)
	setupSD(SPI_bus,pin_cs)
#end def

def setupI2C():
	global I2C_bus
	pin_scl = Pin(3)
	pin_sda = Pin(2)
	I2C_bus = I2C(1, sda=pin_sda, scl = pin_scl, freq=400000)
#end def

def setupVL53():
	global vl53, I2C_bus
	rstHardware()
	for i in range(numSen):
		I2C_bus.writeto(TCA_addr, TCA_dir[i])
		vl53[i] = VL53L0X(I2C_bus)
		vl53[i].set_Vcsel_pulse_period(vl53[i].vcsel_period_type[0], 12)
		vl53[i].set_Vcsel_pulse_period(vl53[i].vcsel_period_type[1], 8)
		#print(f'Sensor {i+1} iniciado')

def setupSensors():
	global sensor, pines
	for i in range(numSen):
		sensor[i] = VL53Rat(limit)
#end def

def setup():
	NeoD[0] = hsv2rgb(150, 1, 0.1)
	NeoD.write()
	setupSPI()
	setupI2C()
	setupVL53()
	setupSensors()
	NeoD[0] = hsv2rgb(150, 1, 0)
	NeoD.write()
#end def

def getInfo():
	global sensor, numSen
	info = []
	for i in range(numSen):
		info.append(sensor[i].returnInfo())
	return info
		#return rat

def writeSD(signal):
	NeoD[0] = hsv2rgb(300, 1, 0.1)
	NeoD.write()
	global bottomEnd, topEnd
	topEnd = getTime()
	data = getInfo()
	try:
		with open("/sd/ratitas.txt", "a") as file:
			file.write(f'\nInicio: {bottomEnd}. Final {topEnd}. ')
			for i in range(len(data)):
				file.write(f'Sujeto{i+1}: {data[i]}. ')
			print('Data writes successfuly')
	except:
		print('Cannot write')
	bottomEnd = topEnd
	NeoD[0] = hsv2rgb(300, 1, 0)
	NeoD.write()
#end def

def main():
	global  I2C_bus, vl53, bottomEnd
	setup()
	signal.init(period=timep*1000, mode=Timer.PERIODIC, callback=writeSD)
	bottomEnd = getTime()
	while True:
		for i in range(numSen):
			I2C_bus.writeto(TCA_addr, TCA_dir[i])
			sensor[i].checkDistance(vl53[i].ping())
#end def

if __name__ == '__main__':
	try:
		NeoD[0] = hsv2rgb(0, 1, 0)
		NeoD.write()
		main()
	except Exception as e:
		signal.deinit()
		print('--- Caught Exception ---')
		import sys
		sys.print_exception(e)
		print('----------------------------')
		if 'EIO' in str(e):
			NeoD[0] = hsv2rgb(122, 1, 0.1)
			NeoD.write()


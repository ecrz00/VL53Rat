from machine import Pin, UART
from time import sleep
from utime import sleep_ms

pin_tx = Pin(17, Pin.OUT)
pin_rx = Pin(16, Pin.IN)
uart   = UART(2, baudrate=115200, tx=17, rx=16, timeout=1, timeout_char=1)
numSen = 2

def read2write(string):
	li = list(string.split(' '))
	info = f'In the lapse between {li[0]} at {li[1]} and {li[2]} at {li[3]}'
	for i in range(numSen):
		info = info + f'\n Sensor {i+1} detected presence for {li[i+4]}'
	print(info)
     

def main():
	while True:
		line = uart.readline()
		if not line: continue
		line = line.decode('utf-8')
		line = line.strip()
		read2write(line)
		
if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print('--- Caught Exception ---')
		import sys
		sys.print_exception(e)
		print('----------------------------')
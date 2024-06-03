from machine import Pin, I2C, Timer
import neopixel
from utime import sleep_ms
from time import sleep
import time
from VL53L0X import VL53L0X

""" Global variables """
imp = None
numSen = 1																		#definimos el número de sensores a usar
miliseg,seg, minu, hrs = [0]*numSen, [0]*numSen, [0]*numSen, [0]*numSen 		#A cada sensor se le asigna su respestiva variable de miliseg, seg, etc.
																				#Para facilidades se crea una lista llena de ceros de longitudd igual a no. sensores

lim, tiempo = 15, 30  															#el tiempo se debe colocar en segundos

extremoInf, extremoSup = [], []													#se definen dos extremos para almacenar los datos del intervalo en el que se realiza cada
																				#medición. Ambos son listas vacías que guardarán como string la fecha y hora

address = [0x29,0x30]

"""-------------------------------------------------- funciones ---------------------------------------------"""
def counter(i):																	#función que lleva la cuenta desde milisegundos hasta horas. Usa las variables globales y
	global miliseg, seg, minu, hrs												#el índice i para alterar el elemento de la lista correspodiente. Usa if's anidados para 
	miliseg[i]+=1																#indicar cúando hacer un cambio en las respectivas unidades.
	if(miliseg[i]==1000):
		seg[i]+=1
		miliseg[i]=0
		if(seg[i]==60):
			minu[i]+=1
			seg[i]=0
			if(minu[i] == 60):
				hrs[i]+=1
				minu[i]=0
				

def getTime():																	#función que optiene la fecha y hora en forma de tuple. Sabiendo el elemento correspondiente
	tup = time.localtime()														#a cadda dato se crea un string con la fecha y otro con la hora. Al final sse regresa la variable
	fecha = str(tup[0]) + '/' + str(tup[1]) + '/' + str(tup[2])
	hora  = str(tup[3]) + ':' + str(tup[4]) + ':' + str(tup[5])
	tiempo = [fecha, hora]
	return tiempo

def end(signal):																#función de se ejecuta al final de la cuenta de signal. Se usa para guardar la información
	global miliseg, seg, minu, hrs, extremoInf, extremoSup						#cada x tiempo. 
	extremoSup = getTime()
	for i in range(numSen):
		print('El sensor ' + str(i+1) + ' detectó presencia durante '+str(hrs[i])+' horas '+str(minu[i])+' minutos '+str(seg[i])+' segundos y '+str(miliseg[i])+' milisegundos del '+str(extremoInf[0])+' a las ' + str(extremoInf[1]) + ' al '+str(extremoSup[0])+' a las ' + str(extremoSup[1]))
		miliseg[i], seg[i], minu[i], hrs[i] = 0, 0, 0, 0
	print('\n')
	extremoInf = extremoSup
	
def sensorUno(i):
	global imp
	tof1.start()
	d=tof1.read()/10
	tof1.stop()
	if d<lim and imp != 'menor':
		timer.init(freq=1000, mode=Timer.PERIODIC, callback=lambda t, id=i: counter(id))
		#print('Se ha detectado algo')
		imp = 'menor'
	elif d>=lim and imp != 'mayor':
		timer.deinit()
		#print('No se ha detectado presencia')
		imp = 'mayor'

"""-------------Inicializa I2C----------------------"""
I2C_bus = I2C(1, sda=Pin(2), scl = Pin(3), freq=400000)

tof1 = VL53L0X(I2C_bus,0x29)


"""-------------Define temporizadores----------------------"""
timer = Timer()
signal = Timer()


"""-------------Inicializaciones previas al bucle----------------------"""

signal.init(period=tiempo*1000, mode=Timer.PERIODIC, callback=end)
extremoInf= getTime()

while True:
	sensorUno(0)

    #q = tof.set_signal_rate_limit(0.1)
    #
    # time.sleep(0.1)
    
    #reloj en tiempo real para saber a que horario corresponde
    #ver si se puede guardar en un archivo de texto,o si los puede pasar a excel, cada día un nuevo archivo o una pestaña
    #que funcione con dos sensores
    #recubrimiento en soldadura para que no haya conductividad
    
 
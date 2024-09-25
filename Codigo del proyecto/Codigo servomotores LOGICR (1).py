import machine
import time
from machine import Pin

servos = [machine.PWM(Pin(i), freq=50, duty=0) for i in [23,21,22,19]]


def map(x, in_min, in_max, out_min, out_max):
   return int((x- in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
def servo (idServo, angle):
    # idServo [0...3] son 4 servos
    servos[idServo].duty(map(angle, 0, 180, 20, 120))

data_pass = None
# Ejecución de función: primero recibe el dato de que servo mover y luego el angulo a mover
def exe(data):
    """datatext = data.decode('uft-8')[:-2] #str(data,´"
    print(datatext)"""
    global data_pass
    if data_pass!= None:
        print("previo")
        """dataint = int(datatext)
        print(dataint*2)"""
        print(data_pass)
        print(data)
        servo(data_pass, data)
        data_pass = None
    elif data in (0,1,2,3,4):
        if data == 0:
            print("Hola")
            print(data_pass)
            data_pass = 0
            print("Hola")
        elif data == 1:
            data_pass = 1
        elif data == 2:
            data_pass = 2
        elif data == 3:
            data_pass = 3
        elif data == 4:
            data_pass = 4
while True:           
    data=int(input("Dato= "))
    exe(data)
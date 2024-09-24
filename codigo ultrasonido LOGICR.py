import machine
import time

trigPin = Pin(33, Pin.OUT)
echoPin = Pin(32, Pin.IN)

def measure_distance():   
    trigPin.off()
    time.sleep_us(2)
    trigPin.on()
    time.sleep_us(10)
    trigPin.off()

  # Medir la duración del pulso en el pin Echo
    while echoPin.value() == 0:
        pass
    start = time.ticks_us()    
    while echoPin.value() == 1:
        pass
    end = time.ticks_us()
    # Calcular la distancia
    duration = time.ticks_diff(end, start)
    distance = (duration * 0.034) / 2
    return distance

while True
   print(measure_distance())
   time.sleep(1)
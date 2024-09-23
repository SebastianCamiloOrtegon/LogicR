import usocket as socket
import asyncio #Comunicación por socket
import ujson
import network #Conexion WIFI
import utime
import machine
import time
import struct #entero a Buffer
#Configuración de servos
from machine import Pin #Motores
servos = [machine.PWM(Pin(i), freq=50, duty=0) for i in [23,21,22,19]]
#Configuración de funciones para motorreductores
# Configurar PWM para EN1, EN2, EN3, EN4
en1 = PWM(Pin(32))
en2 = PWM(Pin(33))
en3 = PWM(Pin(19))
en4 = PWM(Pin(20))
# Establecer la frecuencia PWM en 1 kHz
en1.freq(1000)
en2.freq(1000)
en3.freq(1000)
en4.freq(1000)
#Función velocidad motorreductores
def establecer_velocidad(pin_avance, pin_retroceso, ciclo_trabajo, en_pin):
    # Inicializamos el PWM en los pines de avance y retroceso para el motor
    pwm_avance = PWM(pin_avance)
    pwm_retroceso = PWM(pin_retroceso)

    # Establecemos la frecuencia PWM en 1 kHz
    pwm_avance.freq(1000)
    pwm_retroceso.freq(1000)

    # Aplicamos el ciclo de trabajo para controlar la velocidad
    pwm_avance.duty(ciclo_trabajo)
    pwm_retroceso.duty(0)

    # Activar el pin de habilitación con el mismo ciclo de trabajo
    en_pin.duty(ciclo_trabajo)

# Definición de pines para los motorreductores
# Motorreductor 1 (L293D A)
motor1_avance = Pin(12, Pin.OUT)
motor1_retroceso = Pin(13, Pin.OUT)
# Motorreductor 2 (L293D A)
motor2_avance = Pin(16, Pin.OUT)
motor2_retroceso = Pin(17, Pin.OUT)
# Motorreductor 3 (L293D B)
motor3_avance = Pin(18, Pin.OUT)
motor3_retroceso = Pin(25, Pin.OUT)
# Motorreductor 4 (L293D B)
motor4_avance = Pin(26, Pin.OUT)
motor4_retroceso = Pin(27, Pin.OUT)

# Conexión de ESP32 a red WIFI
"""wf = network.WLAN(network.STA_IF)
wf.active(True)
wf.connect("Redmi Note 9", "maincramaincra")
while not wf.isconnected():
    print(".")
    utime.sleep(1)
print(wf.ifconfig())"""
#Pines sensor ultrasonido
trigPin = Pin(33, Pin.OUT)
echoPin = Pin(32, Pin.IN)
#Función ultrasonido
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
    distanceint = int(distance)
    
    buffer = struct.pack('i', distanceint)
    return buffer

#Envio de datos del ultrasonido a aplicación

async def sendDataPeriodically(conn):
    while True:
        try:
            print("Start send data")
            conn.write("start send data")
            #ultrasonido.measure_distance()																																																																																												
            print("Finish send data")
        except OSError as e:
            print("Error to send data", e)
            break
        await asyncio.sleep(1) # cada segundo envía un dato
#Función mapa para servomotor 
def map(x, in_min, in_max, out_min, out_max):
   return int((x- in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
def servo (idServo, angle):
    # idServo [0...3] son 4 servos
    servos[idServo].duty(map(angle, 0, 180, 20, 120))
    

data_pass = None
# Función para recepción de datos de node red
def exec(data):
    datatext = data.decode('uft-8')[:-2] #Conversión de Buffer a texto
    print(datatext)
    global data_pass
    # data_pass = None
    if data_pass!= None:
        print(data_pass)
        print("previo")
        dataint = int(datatext)
        print(dataint*2)
        servo(data_pass, dataint) #Ejecución de movimiento de servo
        data_pass = None
    #Servos escogidos
    elif datatext in ("s0", "s1", "s2", "s3", "s4"):
        if datatext == "s0":
            print("Hola")
            data_pass = 0
            print("Hola")
        elif datatextd == "s1":
            data_pass = 1
        elif datatext == "s2":
            data_pass = 2
        elif datatext == "s3":
            data_pass = 3
        elif datatext == "s4":
            data_pass = 4
    #Movimientos de LOGICR
    elif datatext == "s9":
        print("Hola")
        # Detiene todos los motorreductores
        establecer_velocidad(motor1_avance, motor1_retroceso, 0, en1)
        establecer_velocidad(motor2_avance, motor2_retroceso, 0, en2)
        establecer_velocidad(motor3_avance, motor3_retroceso, 0, en3)
        establecer_velocidad(motor4_avance, motor4_retroceso, 0, en4)
    elif datatext == "s11":
        print("Hola")
         # Mueve todos los motores hacia adelante al 80% de velocidad
        establecer_velocidad(motor1_avance, motor1_retroceso, 820, en1)
        establecer_velocidad(motor2_avance, motor2_retroceso, 820, en2)
        establecer_velocidad(motor3_retroceso, motor3_avance, 820, en3) # Invertido
        establecer_velocidad(motor4_retroceso, motor4_avance, 820, en4) # Invertido
    elif datatext == "s12":
        print("Hola")
        # Mueve todos los motores hacia atras al 80% de velocidad
        establecer_velocidad(motor1_retroceso, motor1_avance, 820, en1)
        establecer_velocidad(motor2_retroceso, motor2_avance, 820, en2)
        establecer_velocidad(motor3_avance, motor3_retroceso, 820, en3) # Invertido
        establecer_velocidad(motor4_avance, motor4_retroceso, 820, en4) # Invertido
    elif datatext == "s13":
        print("Hola")
        # Motorreductores 2 y 1 hacia adelante, 4 y 3 hacia atrás (IZQUIERDA)
        establecer_velocidad(motor1_avance, motor1_retroceso, 820, en1)
        establecer_velocidad(motor2_avance, motor2_retroceso, 820, en2)
        establecer_velocidad(motor3_avance, motor3_retroceso, 820, en3)
        establecer_velocidad(motor4_avance, motor4_retroceso, 820, en4)
    elif datatext == "s14":
        # Motorreductores 4 y 3 hacia adelante, 2 y 1 hacia atrás (DERECHA)
        establecer_velocidad(motor1_retroceso, motor1_avance, 820, en1)
        establecer_velocidad(motor2_retroceso, motor2_avance, 820, en2)
        establecer_velocidad(motor3_retroceso, motor3_avance, 820, en3)
        establecer_velocidad(motor4_retroceso, motor4_avance, 820, en4)
        print("Hola")
    elif datatext == "s15":
        print("Hola")
        # Motorreductores 1 y 3 hacia adelante, 2 y 4 hacia atrás (GIRO COMPLETO A LA IZQUIERDA)
        establecer_velocidad(motor1_avance, motor1_retroceso, 820, en1)
        establecer_velocidad(motor2_retroceso, motor2_avance, 820, en2)
        establecer_velocidad(motor3_retroceso, motor3_avance, 820, en3)
        establecer_velocidad(motor4_avance, motor4_retroceso, 820, en4)
    elif datatext == "s16":
        print("Hola")
        # Motorreductores 2 y 4 hacia adelante, 1 y 3 hacia atrás (GIRO COMPLETO A LA DERECHA)
        establecer_velocidad(motor1_retroceso, motor1_avance, 820, en1)
        establecer_velocidad(motor2_avance, motor2_retroceso, 820, en2)
        establecer_velocidad(motor3_avance, motor3_retroceso, 820, en3)
        establecer_velocidad(motor4_retroceso, motor4_avance, 820, en4)
    elif datatext == "s17":
        print("Hola")
        # Motorreductores 2 y 3 se mantienen bloqueados, 1 hacia adelante y 4 hacia atrás (GIRO HACIA LA IZQUERDA SOBRE UNA RUEDA)
        establecer_velocidad(motor1_avance, motor1_retroceso, 820, en1)
        establecer_velocidad(motor2_avance, motor2_retroceso, 0, en2)
        establecer_velocidad(motor3_avance, motor3_retroceso, 0, en3)
        establecer_velocidad(motor4_avance, motor4_retroceso, 820, en4)
    elif datatext == "s18":
        print("Hola")
        # Motorreductores 2 y 3 se mantienen bloqueados, 1 hacia atrás y 4 hacia adelante (GIRO HACIA LA DERECHA SOBRE UNA RUEDA)
        establecer_velocidad(motor1_retroceso, motor1_avance, 820, en1)
        establecer_velocidad(motor2_avance, motor2_retroceso, 0, en2)
        establecer_velocidad(motor3_avance, motor3_retroceso, 0, en3)
        establecer_velocidad(motor4_retroceso, motor4_avance, 820, en4)
    """if data == b'A':
        print("Arriba")
    elif data == b'B':
        print("Abajo")
    elif data == b'C':
        print("Izquierda")
    elif data == b'D':
        print("Derecha")
    elif data == b'E':
        print("Detener")
    else:
        print("Otra opcion")"""
#Conexión por socket (NO MODIFICAR)  
class Server:
    def __init__(self, host="0.0.0.0", port=3000, backlog=5, timeout=20):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.timeout = timeout

    async def run(self):
        print("Awaiting client connection.")
        self.cid = 0
        # asyncio.create_task(heartbeat(100))
        self.server = await asyncio.start_server(
            self.run_client, self.host, self.port, self.backlog
        )
        while True:
            await asyncio.sleep(100)

    async def run_client(self, sreader, swriter):
        self.cid += 1
        print("Got connection from client", self.cid)
        asyncio.create_task(sendDataPeriodically(swriter))
        try:
            while True:
                try:
                    res = await asyncio.wait_for(sreader.readline(), self.timeout)
                except asyncio.TimeoutError:
                    res = b""
                if res == b"":
                    raise OSError
                # print("Received {} from client {}".format(ujson.loads(res.rstrip()), self.cid))
                print("Data Received: ", res)
                exec(res)
                swriter.write(res)
                await swriter.drain()  # Echo back"""
        except OSError:
            pass
        print("Client {} disconnect.".format(self.cid))
        await sreader.wait_closed()
        print("Client {} socket closed.".format(self.cid))

    async def close(self):
        print("Closing server")
        self.server.close()
        await self.server.wait_closed()
        print("Server closed.")


server = Server()
try:
    asyncio.run(server.run())
except KeyboardInterrupt:
    print("Interrupted")  # This mechanism doesn't work on Unix build.
finally:
    asyncio.run(server.close())
    _ = asyncio.new_event_loop()
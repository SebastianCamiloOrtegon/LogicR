from machine import Pin, PWM
import time

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

def detener():
    # Detiene todos los motorreductores
    establecer_velocidad(motor1_avance, motor1_retroceso, 0, en1)
    establecer_velocidad(motor2_avance, motor2_retroceso, 0, en2)
    establecer_velocidad(motor3_avance, motor3_retroceso, 0, en3)
    establecer_velocidad(motor4_avance, motor4_retroceso, 0, en4)

def mover_adelante():
    # Mueve todos los motores hacia adelante al 80% de velocidad
    establecer_velocidad(motor1_avance, motor1_retroceso, 820, en1)
    establecer_velocidad(motor2_avance, motor2_retroceso, 820, en2)
    establecer_velocidad(motor3_retroceso, motor3_avance, 820, en3) # Invertido
    establecer_velocidad(motor4_retroceso, motor4_avance, 820, en4) # Invertido

def mover_atras():
    # Mueve todos los motores hacia atrás al 80% de velocidad
    establecer_velocidad(motor1_retroceso, motor1_avance, 820, en1)
    establecer_velocidad(motor2_retroceso, motor2_avance, 820, en2)
    establecer_velocidad(motor3_avance, motor3_retroceso, 820, en3) # Invertido
    establecer_velocidad(motor4_avance, motor4_retroceso, 820, en4) # Invertido

def girar_izquierda():
    # Motorreductores 2 y 1 hacia adelante, 4 y 3 hacia atrás
    establecer_velocidad(motor1_avance, motor1_retroceso, 820, en1)
    establecer_velocidad(motor2_avance, motor2_retroceso, 820, en2)
    establecer_velocidad(motor3_avance, motor3_retroceso, 820, en3)
    establecer_velocidad(motor4_avance, motor4_retroceso, 820, en4)

def girar_derecha():
    # Motorreductores 4 y 3 hacia adelante, 2 y 1 hacia atrás
    establecer_velocidad(motor1_retroceso, motor1_avance, 820, en1)
    establecer_velocidad(motor2_retroceso, motor2_avance, 820, en2)
    establecer_velocidad(motor3_retroceso, motor3_avance, 820, en3)
    establecer_velocidad(motor4_retroceso, motor4_avance, 820, en4)

def giro_completo_izquierda():
    # Motorreductores 1 y 3 hacia adelante, 2 y 4 hacia atrás
    establecer_velocidad(motor1_avance, motor1_retroceso, 820, en1)
    establecer_velocidad(motor2_retroceso, motor2_avance, 820, en2)
    establecer_velocidad(motor3_retroceso, motor3_avance, 820, en3)
    establecer_velocidad(motor4_avance, motor4_retroceso, 820, en4)

def giro_completo_derecha():
    # Motorreductores 2 y 4 hacia adelante, 1 y 3 hacia atrás
    establecer_velocidad(motor1_retroceso, motor1_avance, 820, en1)
    establecer_velocidad(motor2_avance, motor2_retroceso, 820, en2)
    establecer_velocidad(motor3_avance, motor3_retroceso, 820, en3)
    establecer_velocidad(motor4_retroceso, motor4_avance, 820, en4)

def giro_izquierda_rueda():
    # Motorreductores 2 y 3 se mantienen bloqueados, 1 hacia adelante y 4 hacia atrás
    establecer_velocidad(motor1_avance, motor1_retroceso, 820, en1)
    establecer_velocidad(motor2_avance, motor2_retroceso, 0, en2)
    establecer_velocidad(motor3_avance, motor3_retroceso, 0, en3)
    establecer_velocidad(motor4_avance, motor4_retroceso, 820, en4)

def giro_derecha_rueda():
    # Motorreductores 2 y 3 se mantienen bloqueados, 1 hacia atrás y 4 hacia adelante
    establecer_velocidad(motor1_retroceso, motor1_avance, 820, en1)
    establecer_velocidad(motor2_avance, motor2_retroceso, 0, en2)
    establecer_velocidad(motor3_avance, motor3_retroceso, 0, en3)
    establecer_velocidad(motor4_retroceso, motor4_avance, 820, en4)

if __name__ == '__main__':
    try:
        mover_adelante()  
        time.sleep(2) 
        detener()  
        
        mover_atras() 
        time.sleep(2)  
        detener()  
        
        girar_izquierda()  
        time.sleep(2) 
        detener() 
        
        girar_derecha()  
        time.sleep(2) 
        detener() 
        
        giro_completo_izquierda()  
        time.sleep(2) 
        detener()  
        
        giro_completo_derecha() 
        time.sleep(2) 
        detener() 
        
        giro_izquierda_rueda()
        time.sleep(2)  
        detener()  
        
        giro_derecha_rueda()  
        time.sleep(2)  
        detener()  
        
    finally:
        detener() 
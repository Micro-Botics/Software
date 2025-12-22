from mpu6050 import MPU6050
from machine import PWM, Pin
import time

# Configurar pines del motor puente H
MOTOR_IN1 = Pin(16, Pin.OUT)
MOTOR_IN2 = Pin(17, Pin.OUT)
MOTOR_PWM = PWM(Pin(18), freq=1000)

# Configurar acelerómetro
i2c = machine.I2C(0, scl=Pin(21), sda=Pin(20))
mpu = MPU6050(i2c)

METROS_A_PULSOS = 0.05  # Ajustar según calibración

def adelante(metros):
    """
    Mueve el robot hacia adelante una distancia especificada en metros.
    
    Args:
        metros: distancia a recorrer en metros
    """
    distancia_target = metros
    distancia_actual = 0
    velocidad_anterior = 0
    
    # Activar motor en dirección adelante
    MOTOR_IN1.on()
    MOTOR_IN2.off()
    MOTOR_PWM.duty_u16(50000)  # 75% potencia
    
    while distancia_actual < distancia_target:
        # Leer aceleración en eje X
        accel = mpu.get_accel_data()
        ax = accel['x']
        
        # Integrar aceleración para obtener velocidad (m/s)
        velocidad = (ax + velocidad_anterior) / 2
        
        # Integrar velocidad para obtener distancia
        distancia_actual += abs(velocidad) * 0.01  # dt = 10ms
        
        velocidad_anterior = velocidad
        time.sleep(0.01)
    
    # Detener motor
    MOTOR_PWM.duty_u16(0)
    MOTOR_IN1.off()
    MOTOR_IN2.off()
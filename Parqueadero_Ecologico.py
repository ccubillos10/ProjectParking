#Modulos Importados
from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
import time, network
import framebuf
from random import randrange

#Se crean objetos y variables

entradap = Pin(2, Pin.IN, Pin.PULL_DOWN)  #Sensor infrarojo
salidap = Pin(4, Pin.IN, Pin.PULL_DOWN)   #Sensor infrarojo

ancho = 128                               # Pantalla Oled
alto = 64                                 # Pantalla Oled
i2c = I2C(0, scl=Pin(22), sda=Pin(21))    # Pantalla Oled
oled = SSD1306_I2C(ancho, alto, i2c)      # Pantalla Oled
print(i2c.scan())                         # Pantalla Oled

servo = PWM(Pin(15), freq=50)             # Servomotor

espacios={1:True,2:True,3:True,4:True,5:True,6:True,7:True,8:True,9:True,10:True} #Creación de diccionario
disponibilidad=len(espacios)              #Cantidad de espacios en el parqueadero
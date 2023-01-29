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

    #Funcion para cambiar resolucion de servomotor a grados

def map(x):
        return int((x - 0) * (125-25) / (180 - 0) + 25)

    #Funcion para conectarse a WIFI
def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True

    #Ejecucion de la funcion Wifi
if conectaWifi ("CONEXION_DUQUE", "G1a2d3r41927"):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    
    #Función para asignar una ubicación disponible en el parqueadero
def asignar_ubicacion(v):
    for ubicacion, disponible in espacios.items(): # Realiza la revision de cada elemento en el diccionario
        if disponible:                             # Al encontrar una ubicacion con el valor de True(Libre) ingresa a esta opción
            global disponibilidad
            disponibilidad -= 1                    # Resta en la variable disponibilidad la cantidad de ubicaciones disponibles
            espacios[ubicacion] = False            # Realiza el cambio de estado True a False de la ubicacion seleccionada
            m = map(0)                             # Grados del servomotor (abierto)
            servo.duty(m)
            oled.fill(0)                           # Imprime en la pantalla oled la ubicacion a donde se tiene que estacionar
            oled.text("*************",10,0)
            oled.text("Estacione en ",10,10)
            oled.text("la ubicacion",10,20)
            oled.text(str(ubicacion),57,30)
            oled.text("*************",10,50)
            oled.show()
            break
            time.sleep(2)
    else:                                           # Cuando no se encuentra un valor True en las ubicaciones se ejecuta esta opción
        print("Parqueadero Lleno")
        oled.fill(0)                                # Indica en la pantalla oled que no se tiene cupo en el parqueadero
        oled.text("*************",10,0)
        oled.text("Lo sentimos!",10,20)
        oled.text("Estamos",35,30)
        oled.text("Sin Cupo",30,40)
        oled.text("*************",10,50)
        oled.show()
        time.sleep(2)

    #Función para liberar una ubicación en el parqueadero
def liberar_ubicacion(verificacion):
    for ubicacion, disponible in espacios.items():  # Realiza la revision de cada elemento en el diccionario
        if not disponible:                          # Al encontrar una ubicacion con el valor de False(Ocupado) ingresa a esta opción
            global disponibilidad
            disponibilidad += 1                     # Adiciona en la variable disponibilidad la cantidad de ubicaciones disponibles
            espacios[ubicacion] = True              # Realiza el cambio de estado False a True de la ubicacion seleccionada
            m = map(0)                              # Grados del servomotor (abierto)
            servo.duty(m)
            print(f"La ubicación {ubicacion} ha sido liberada")
            break
            time.sleep(2)        
            
    #Ejecucion Inicial
while True:
    oled.fill(0)                              # Indica en la pantalla oled el nombre del parqueadero y la disponibilidad de este
    oled.text("*************",10,0)
    oled.text("Paqueadero",20,10)
    oled.text("Ecologico",25,20)        
    oled.text("*************",10,30)
    oled.text("Disponibles",20,40)
    oled.text(str(disponibilidad),57,50)
    oled.show()
    #print(espacios)                          #Impresion de prueba diccionario
    #print(disponibilidad)                    #Impresion de prueba variable
    
    if entradap.value() == 0:    # Sensor infrarojo de entrada si detecta objeto
        oled.fill(0) 
        oled.text("*************",10,0)
        oled.text("Ingresando",20,20)
        oled.text("Vehiculo",30,30)            
        oled.text("*************",10,50)
        oled.show()
        print("Movimiento detectado Entrada")
        verificacion=randrange(10)
        asignar_ubicacion(verificacion)
        time.sleep(5)
            
    elif salidap.value() == 0:    # Sensor infrarojo de salida si detecta objeto   
        oled.fill(0) 
        oled.text("*************",10,0)
        oled.text("Saliendo",30,20)
        oled.text("Vehiculo",30,30)            
        oled.text("*************",10,50)
        oled.show()          
        print("Movimiento detectado Salida")
        if disponibilidad<10:  # Si se encuentra ocupadas todas las ubicaciones del parqueadero ejecuta la funcion liberar ubicacion 
            liberar_ubicacion(verificacion)
        else:                  # Si se encuentran disponibles todas las ubicaciones y se activa el sensor de salida,
                               # Este indicara indica que no se encuntran vehiculos en el parqueadero y no ejecutara accion en el sevomotor            
            print("Parqueadero vacio")
            oled.fill(0) 
            oled.text("*************",10,0)
            oled.text("Parqueadero",20,20)
            oled.text("Vacio",40,30)            
            oled.text("*************",10,50)
            oled.show()
        time.sleep(5)
                  
    else:
        print("Sin movimiento")    
        m = map(90)  #Grados del servomotor (cerrado)
        servo.duty(m)
        time.sleep(1)    
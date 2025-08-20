#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


morgru = EV3Brick()
morgru.light.on(Color.ORANGE)
right_motor = Motor(Port.D)
left_motor = Motor(Port.B)
right_sensor = ColorSensor(Port.S1)
left_sensor = ColorSensor(Port.S4)
end_sensor = ColorSensor(Port.S3)


min_value = 6
max_value = 40

speed = 60 
#spd = 80, kp, ki, kd = -1.1,-0.022, -3
kp, ki, kd = 0.65,0.022,15
precisao = 1
erro = 0
i_value, d_value = 0, 0
last_error = 0
u = 0
tempo = StopWatch()
tempo_pista = StopWatch()
dps_final = 600
counter, max_counter, = 0, 4
acabar = False
p, i, d = 0, 0, 0

cavalo = 0 #nunca apagar


while True:
    
    if (left_sensor.reflection() > 30) and (right_sensor.reflection() > 30):
        tempo.reset()
        
    tempo_parada = tempo.time()
    
    if end_sensor.reflection() > 30 and counter == 0:
        tempo.reset()
        tempo_pista.reset()
        counter += 1
        
    elif end_sensor.reflection() > 30 and tempo_parada > 1000 and counter != 0:
        tempo.reset()
        acabar = True 
        
    r = right_sensor.reflection()
    l = left_sensor.reflection()
    
    if r>30:
        r = max(r,max_value)
    if l>30:
        l = max(l,max_value)
    if r<10:
        r = min(r,min_value)
    if l<10:
        l = min(l,min_value)
        
    # Codigo do seguidor de linha
    esqM = 0
    dirM = 0


    esqM = left_sensor.reflection()
    dirM = right_sensor.reflection()
    esqM = max(min_value, esqM)
    esqM = min(max_value, esqM)
    dirM = max(min_value, dirM)
    dirM = min(max_value, dirM)
    
    erro = dirM - esqM 
    i_value += erro
    d_value = erro - last_error
    last_error = erro
    p, i, d = (erro * kp), (i_value * ki), (d_value * kd)
    
    u = p + i + d
    if((right_sensor.reflection() > 30 and left_sensor.reflection() > 30)):
        u = 0     
            
    l_speed, r_speed = (-1 * (speed + u)), (speed - u)
    """
    l_speed = min(0,l_speed)
    r_speed = max(0,r_speed)
    """
    
    left_motor.dc(l_speed)
    right_motor.dc(r_speed)
    
    tempo_parada = tempo.time()
    
    if acabar == True and tempo_parada > 300:
        tempo_gasto = str(tempo_pista.time())
        print("         Gastou: " + tempo_gasto)
        break 
right_motor.dc(0)
left_motor.dc(0)
morgru.screen.print(tempo_gasto)
wait(10000)

#sensor direito linha = +
#sensor esquerdo linha = -
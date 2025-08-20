#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,InfraredSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


morgru = EV3Brick()
morgru.light.on(Color.ORANGE)
right_sensor = ColorSensor(Port.S1)
left_sensor = ColorSensor(Port.S4)
end_sensor = ColorSensor(Port.S3)



tempo_calibragem = StopWatch()
calibrate_time = 0
right_motor = Motor(Port.D)
left_motor = Motor(Port.B)

cavalo = 0 #nunca apagar

minl = 0
maxl = 0
minr = 0
maxr = 0

ming = 0
maxg = 0

x = 1
while calibrate_time < 5000:
    right_motor.dc((50 * x))
    left_motor.dc((-50 * x))
    
    l = left_sensor.reflection()
    r = right_sensor.reflection()
    
    if minl == 0 or maxr == 0:
        minl, maxl = l,l    
        minr, maxr = r,r   
    
    else:
        minl = min(minl, l)
        minr = min(minr, r)
        maxl = max(maxl, l)
        maxr = max(maxr, r)
        ming = max(minl,minr)
        maxg = min(maxl,maxr)
        
    calibrate_time = tempo_calibragem.time()
    x = x * -1
    wait(500)
print(ming)
print(maxg)
morgru.screen.print(ming)
morgru.screen.print(maxg)
right_motor.dc(0)
left_motor.dc(0)
wait(10000)
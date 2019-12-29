#!/usr/bin/python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
precision = 3
try:
    tFile = open('/sys/class/thermal/thermal_zone0/temp')
    temp = float(tFile.read())
    tempC = temp/1000
    if tempC > 43.5:
        GPIO.output(17, 1)
        print('CPU Temp: ', tempC, 'Celsius')
        print('Warm')
        GPIO.cleanup()
    else:
        GPIO.output(17, 0)
        print('CPU Temp: ',"{:.{}f}".format( tempC,precision ), 'Celsius')
        print('Cold')
        GPIO.cleanup()
except:
    tFile.close()
    GPIO.cleanup()
    exit
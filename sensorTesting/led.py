//simple code to turn an LED on / off

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT) 

while True:
  GPIO.output(17,GPIO.HIGH) //led array on
  time.sleep(5)
  GPIO.output(18,GPIO.LOW) //led array off
  time.sleep(5)

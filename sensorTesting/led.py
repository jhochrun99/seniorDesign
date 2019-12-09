#simple code to turn an LED on / off

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
PIN = 17
GPIO.setup(PIN, GPIO.OUT) 

while True:
  GPIO.output(PIN, GPIO.HIGH) #led array on
  time.sleep(5)
  GPIO.output(PIN, GPIO.LOW) #led array off
  time.sleep(5)

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
PIN = 18
GPIO.setup(PIN, GPIO.OUT) 

while True:
  GPIO.output(PIN, GPIO.HIGH) #motor on
  time.sleep(5)
  GPIO.output(PIN, GPIO.LOW) #motor off
  time.sleep(5)

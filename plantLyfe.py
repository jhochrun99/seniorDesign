#puts all our sensor testing code into individual functions

import time
import random
# import RPi.GPIO as GPIO
# import busio
# import digitalio

# import board
# from board import SCL, SDA 

# import Adafruit_DHT
# import Adafruit_Nokia_LCD as LCD
# import Adafruit_GPIO.SPI as SPI
# import adafruit_mcp3xxx.mcp3008 as MCP
# from adafruit_mcp3xxx.analog_in import AnalogIn
# from adafruit_seesaw.seesaw import Seesaw

# from PIL import Image
# from PIL import ImageDraw
# from PIL import ImageFont

#code for testing the LED array --------------------------------------------------------
def turnOnLED():
  GPIO.setmode(GPIO.BCM)
  PIN = 17
  GPIO.setup(PIN, GPIO.OUT) 

  while True:
    print("LED On") # GPIO.output(PIN, GPIO.HIGH) #led array on
    time.sleep(5)
    #print("LED Off") # GPIO.output(PIN, GPIO.LOW) #led array off
    #time.sleep(5)
    
def turnOffLED():
  GPIO.setmode(GPIO.BCM)
  PIN = 17
  GPIO.setup(PIN, GPIO.OUT) 
  
  while True:
    print("LED Off") # GPIO.output(PIN, GPIO.LOW) #led array off
    time.sleep(5)

#code for testing the motor ------------------------------------------------------------
def turnOnMotor():
  GPIO.setmode(GPIO.BCM)
  PIN = 18
  GPIO.setup(PIN, GPIO.OUT) 

  while True:
    print("Motor On") # GPIO.output(PIN, GPIO.HIGH) #motor on
    time.sleep(5)
    print("Motor Off") # GPIO.output(PIN, GPIO.LOW) #motor off
    time.sleep(5)

#code for testing the soil sensor ------------------------------------------------------
def getSoilReading():
  return random.uniform(70, 100) # i2c_bus = busio.I2C(SCL, SDA)
  ss = Seesaw(i2c_bus, addr=0x36)
  
  # read moisture level through capacitive touch pad
  touch = ss.moisture_read()
  # read temperature from the temperature sensor
  temp = ss.get_temp()

  print("temp: " + str(temp) + " moisture: " + str(touch))
  # time.sleep(1)
  return touch

#code for testing the humidity/temperature sensor --------------------------------------
def getHumidityTemperatureReading():
  return random.uniform(30, 80), random.uniform(50, 90) # DHT_PIN = 4
  sensor = Adafruit_DHT.DHT11

  humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_PIN)
  if humidity is not None and temperature is not None:
      print("Temp={0:0.1f}*C Humidity={1:0.1f}%".format(temperature, humidity))
  else:
      print("Failed to read.")
  return humidity, temperature
  

#code for testing the force sensitive resistor and the photoresistor -------------------
def getFSRandPRreading():
  return random.randint(100, 140), random.randint(100, 140)
  # create the spi bus
  spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
  # create the cs (chip select)
  cs = digitalio.DigitalInOut(board.D5)
 
  # create the mcp object
  mcp = MCP.MCP3008(spi, cs)
  # create an analog input channel on pin 0
  chan_FSR = AnalogIn(mcp, MCP.P0)

  print('FSR Raw ADC Value: ', chan_FSR.value)
  print('FSR ADC Voltage: ' + str(chan_FSR.voltage) + 'V\n')
  time.sleep(1)
  
  chan_PR = AnalogIn(mcp, MCP.P1)
  print('PR Raw ADC Value: ', chan_PR.value)
  print('PR ADC Voltage: ' + str(chan_PR.voltage) + 'V\n')
  # time.sleep(1)
  return chan_FSR.value, chan_PR.value

#code for watering the plant ---------------------------------------------------------
def waterPlant(soilMoisture, waterAt):
  if(soilMoisture <= waterAt): #value would be based on soil moisture readings from the soil sensor
    print('Plant watered')
    #turnOnMotor() #water the plant

#code for when water container is getting low ----------------------------------------
def refillWater(containerWeight):
    if(containerWeight <= 65): #value would be based on weight of empty container and FSR reading values
      print('refill water container')
      return true
    else
      print('container has enough water')
      return false

#more functions as needed
def gettingLight(lightValue):
  if(lightValue > 40):
    print('Plant is getting light)
    return true
  else:
    print('Plant is not getting light)
    return false

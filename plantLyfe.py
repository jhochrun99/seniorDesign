#puts all our sensor testing code into individual functions

import time
import RPi.GPIO as GPIO
import busio
import digitalio

import board
from board import SCL, SDA 

import Adafruit_DHT
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from adafruit_seesaw.seesaw import Seesaw

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#code for testing the LED array --------------------------------------------------------
def turnOnLED():
  GPIO.setmode(GPIO.BCM)
  PIN = 17
  GPIO.setup(PIN, GPIO.OUT) 

  while True:
    GPIO.output(PIN, GPIO.HIGH) #led array on
    time.sleep(5)
    GPIO.output(PIN, GPIO.LOW) #led array off
    time.sleep(5)

#code for testing the motor ------------------------------------------------------------
def turnOnMotor():
  GPIO.setmode(GPIO.BCM)
  PIN = 18
  GPIO.setup(PIN, GPIO.OUT) 

  while True:
    GPIO.output(PIN, GPIO.HIGH) #motor on
    time.sleep(5)
    GPIO.output(PIN, GPIO.LOW) #motor off
    time.sleep(5)

#code for testing the soil sensor ------------------------------------------------------
def getSoilReading():
  i2c_bus = busio.I2C(SCL, SDA)
  ss = Seesaw(i2c_bus, addr=0x36)

  while True:
    # read moisture level through capacitive touch pad
    touch = ss.moisture_read()
    # read temperature from the temperature sensor
    temp = ss.get_temp()
  
    print("temp: " + str(temp) + " moisture: " + str(touch))
    time.sleep(1)

#code for testing the humidity/temperature sensor --------------------------------------
def getHumidityReading():
  DHT_PIN = 4
  sensor = Adafruit_DHT.DHT11

  while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Failed to read.")

#code for testing the force sensitive resistor and the photoresistor -------------------
def getFSRandPRreading():
  # create the spi bus
  spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
  # create the cs (chip select)
  cs = digitalio.DigitalInOut(board.D5)
 
  # create the mcp object
  mcp = MCP.MCP3008(spi, cs)
  while True: 
    # create an analog input channel on pin 0
    chan = AnalogIn(mcp, MCP.P0)
 
    print('FSR Raw ADC Value: ', chan.value)
    print('FSR ADC Voltage: ' + str(chan.voltage) + 'V\n')
    time.sleep(1)
    
    chan = AnalogIn(mcp, MCP.P1)
    print('PR Raw ADC Value: ', chan.value)
    print('PR ADC Voltage: ' + str(chan.voltage) + 'V\n')
    time.sleep(1)

#code for testing the LCD ---------------------------------------------------------------
def testLCD():
  # Raspberry Pi hardware SPI config:
  DC = 5
  RST = 6
  SPI_PORT = 0
  SPI_DEVICE = 0
  
  disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
  disp.begin(contrast=40)
  disp.clear()
  disp.display()
  
  image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
  draw = ImageDraw.Draw(image)
  draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
  draw.ellipse((2,2,22,22), outline=0, fill=255)
  draw.rectangle((24,2,44,22), outline=0, fill=255)
  draw.polygon([(46,22), (56,2), (66,22)], outline=0, fill=255)
  draw.line((68,22,81,2), fill=0)
  draw.line((68,2,81,22), fill=0)
  
  font = ImageFont.load_default()
  draw.text((8,30), 'Hello World!', font=font)
  
  # Display image.
  disp.image(image)
  disp.display()
  
  print('Press Ctrl-C to quit.')
  while True:
    time.sleep(1.0)

#includes all basic function calls from plantLyfe for an example showing

from plantLyfe
import turnOnLED, turnOnMotor, getSoilReading, getHumidityReading, getFSRandPRreading, testLCD
import time

def main(): 
  getHumidityReading()
  time.sleep(5)
  
  getSoilReading()
  time.sleep(5)
  
  getFSRandPRreading()
  time.sleep(5)
  
  turnOnLED()
  time.sleep(5)
  
  testLCD()
  time.sleep(5)

main()

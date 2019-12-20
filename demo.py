#includes all basic function calls from plantLyfe for an example showing

from plantLyfe import *

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

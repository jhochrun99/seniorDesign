#pseudo code for the logic we'll need later when getting values from the sensors
#basil ideal conditions: 6-8 hr sunlight, water when soil is dry to touch (keep moist soil),
#                        70s for temp, don't allow to get too much lower than 70,
#                        dry air is bad, so mid humidity

#soil sensor deadings: 200 (very dry) to 2000 (very wet)
#returns true if plant needs to be watered
def waterPlantCheck(int moistsure):
  return moisture <= 650
  
#returns true if water needs to be refilled
#value used is guessed - would be based on how heavy the container is when empty
def refillWaterCheck(float fsrReading):
  return fsrReading <= 55
  
#returns -1 if temp is too low, 1 if temp is too high, 0 if neutral
def plantTempCheck(float temperature):
  if(temperature >= 80):
    return 1
  else if(temperature < 70):
    return -1
  else
    return 0
    
#returns false if humidity is too low (dry)
#value is guessed based on data sheet, humidity should be RH % value, lower % = drier
def plantHumidityCheck(float humidity):
  if(humidity < 55):
    return false;

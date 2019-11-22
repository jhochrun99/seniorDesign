//***************************************Jessica Hochrun, Tara Umesh********************************
//basic function definitions using info from sensors, and determining what the plant needs

//uses soil sensor reading to determine if plant needs to be watered 
//200 = very dry, 2000 = very wet
bool supplyWater(int soilMoisture) { ... }

//lets user know if the plant is in optimal tempurature, or if it needs higher/lower temperature
//too cold (-1), good (0), hot (1)
int plantTemperature(int temp) { ... }

//lets user know if the plant is in optimal humidity, or if it needs more/less humidity
//too low (-1), good (0), too high (1)
int plantHumidity(int humidity) { ... }

//keeps track of how much light the plant is getting
int lightReading(int intensity) { ... }

//determines if plant has gotten enough light for the day, based off lightReading
bool supplyLight(int lightRecieved) { ... }

//turns on supplemental light for given duration
void turnOnLight(int duration) { ... }

//uses ultrasonic sensor to get distance to plant, tracking how much plant is growing
int plantGrowth(int height) { ... }

//takes in reading from force sensor to determine if water container needs refilling
bool refillWater(int weight) { ... }

//takes in answer from supplyWater, to determine if plant needs to be watered
//returns true if plant is successfully watered - return is simply for making sure system is working
bool waterPlant(bool needsWater) { ... }

//display info on LCD
//to be displayed: temperature, humidity, water container level, light levels, supplemental light/water supplied
//would need to take this info through as parameter, or have access to variables containing info in a class
void displayInfo(...) { ... }

//Might need to: determine how much water plant needs, how much light plant needs

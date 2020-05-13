from flask import Flask, redirect, render_template, request
from threading import Thread
from plantLyfe import *
import time
import sqlite3

app = Flask(__name__, static_folder='')

# Constants
sun_options = ["Full Sun", "Partial Sun", "Partial Shade", "Full Shade"]
sun_hours = [8, 5, 2, 0]
soil_options = ["Moist", "Normal", "Dry"]
soil_values = [3000, 2000, 1000, 0]

# Globals

# Measurements
soil = 0
temperature = 0
humidity = 0
light_level = 0
water_level = 0

# Settings
light_needs = 3 # 0 hours
moisture_needs = 3 # no moisture 
temperature_low = -100 # will never be this low
temperature_high = 200 # will never be this high
plant_exists = False

# Status
amount_of_light = 0 #will be a float corresponding to hours of light, measured in 30 minute intervals 
led_on = False #keeps track of if LED array has been turned on or not

@app.route("/")
def home():
    global light_needs, moisture_needs, temperature_low, temperature_high, plant_exists, sun_options, soil_options

    with sqlite3.connect("plantlyfeDB.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Plants WHERE active=1")
        current_plant = c.fetchone()
        if (current_plant != None):
            plantName = current_plant[0]
            light_needs = current_plant[2]
            moisture_needs = current_plant[3]
            temperature_low = current_plant[4]
            temperature_high = current_plant[5]
            plantInfo = (sun_options[light_needs], soil_options[moisture_needs], temperature_low, temperature_high)
            plantMeasurement = (current_plant[1], soil, temperature, humidity, light_level, water_level)
            plant_exists = True
        else:
            plantName = "No current plant"
            plantInfo = None
            plantMeasurement = (0, soil, temperature, humidity, light_level, water_level)
            plant_exists = False
        
    return render_template('index.html', plantName=plantName, plantData=plantMeasurement, plantNeeds=plantInfo)

@app.route("/newplant")
def addplant():
    return render_template('new_plant.html')

@app.route("/newplantentry",  methods=["POST"])
def newplantentry():
    if request.form:
        plantData = request.form
        plantName = plantData["plantName"]
        sunlight = plantData["sunlight"]
        soilMoisture = plantData["soilMoisture"]
        lowestTemp = plantData["lowestTemp"]
        highestTemp = plantData["highestTemp"]
        # timeStamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
        with sqlite3.connect("plantlyfeDB.db") as conn:
            c = conn.cursor()
            
            c.execute("SELECT MAX(plantID) FROM Plants")
            plantID_max = c.fetchone()
            if (plantID_max[0] != None):
                plantID = plantID_max[0] + 1
            else:
                plantID = 1
            
            # Sets previously active entries to be false
            c.execute("UPDATE Plants SET active=0 WHERE active=1")

            entry = (plantName, plantID, sunlight, soilMoisture, lowestTemp, highestTemp, 1)
            c.execute("INSERT INTO Plants VALUES (?, ?, ?, ?, ?, ?, ?)", entry)
            conn.commit()
    else:
        print("NO REQUEST")
    return redirect("/")

@app.route("/editplant")
def editplant():
    with sqlite3.connect("plantlyfeDB.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Plants WHERE active=1")
        current_plant = c.fetchone()
        print(current_plant)
        if (current_plant != None):
            plantName = current_plant[0]
        else:
            plantName = "No current plant"
        print(current_plant)
    return render_template('edit_plant.html', plantName=plantName, plantNeeds=current_plant)

@app.route("/editplantentry",  methods=["POST"])
def editplantentry():
    if request.form:
        plantData = request.form
        plantName = plantData["plantName"]
        sunlight = plantData["sunlight"]
        soilMoisture = plantData["soilMoisture"]
        lowestTemp = plantData["lowestTemp"]
        highestTemp = plantData["highestTemp"]
        plantID = plantData["plantID"]
        
        with sqlite3.connect("plantlyfeDB.db") as conn:
            c = conn.cursor()
            entry = (sunlight, soilMoisture, lowestTemp, highestTemp, plantID)
            c.execute("UPDATE Plants SET sunlight=?, soilMoisture=?, lowestTemp=?, highestTemp=? WHERE plantID=?", entry)
            conn.commit()

    return redirect("/")

@app.route("/deleteplant")
def deleteplant():
    with sqlite3.connect("plantlyfeDB.db") as conn:
            c = conn.cursor()
            c.execute("UPDATE Plants SET active=0 WHERE active=1")
            conn.commit()

    light_needs = 3 # 0 hours
    moisture_needs = 3 # no moisture 
    temperature_low = -100 # will never be this low
    temperature_high = 200 # will never be this high
    plant_exists = False
    return redirect("/")


def log_measurement(soil, humidity, temperature, water_level, light_level):
    with sqlite3.connect("plantlyfeDB.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Plants WHERE active=1")
        current_plant = c.fetchone()
        if (current_plant != None):
            measurement = (current_plant[1], soil, humidity, temperature, water_level, light_level, time.strftime('%Y-%m-%d %H:%M:%S'))
            c.execute("INSERT INTO PlantMeasurements VALUES (?, ?, ?, ?, ?, ?, ?)", measurement)
            conn.commit()

def take_measurements(sleep_time):
    global soil, humidity, temperature, water_level, light_level
    while True:
        soil  = round(getSoilReading(), 2)
        humidity, temperature = getHumidityTemperatureReading()
        temperature = round(temperature, 2)
        humidity = round(humidity, 2)
        water_level, light_level = getFSRandPRreading()
        log_measurement(soil, temperature, humidity, light_level, water_level)
        time.sleep(sleep_time)
        
def check_actions(sleep_time):
    while True:
        waterPlant(soil, soil_values[moisture_needs])
        refillWater(water_level)
        time.sleep(sleep_time)
    
def check_light(): #should run every 30 minutes
    while True:
        if(light_level > 45):
            amount_of_light += 0.5
        
        current_time = time.localtime()
        #if light is off, it's past 8pm, and plant hasn't gotten enough light
        if(not led_on and current_time[tm_hour] >= 20 and amount_of_light < sun_hours[light_needs]): #replace 8 with how many of hours of light the plant needs
            turnOnLED()
            led_on = True
        #if plant has enough light and led is on
        elif(amount_of_light >= light_level and led_on):
            turnOffLED()
            led_on = False
            reset_light_count()
        time.sleep(30)
        
def reset_light_count():
    amount_of_light = 0
        
if __name__ == "__main__":
    t1 = Thread(target=take_measurements, args=[1])
    t1.start()
    t2 = Thread(target=check_actions, args=[1])
    t2.start()
    t3 = Thread(target=check_light, args=[])
    t3.start()
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
    t1.join()
    t2.join()
    t3.join()
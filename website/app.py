from flask import Flask, redirect, render_template, request
from threading import Thread
from plantLyfe import *
import time
import sqlite3

app = Flask(__name__, static_folder='')

# Constants
sun_options = ["Full Sun", "Partial Sun", "Partial Shade", "Full Shade"]
soil_options = ["Moist", "Normal", "Dry"]

# Globals
soil = 0
temperature = 0
humidity = 0
light_needs = 0
water_level = 0

@app.route("/")
def home():
    # Do some operations to find these values
    # take_measurements(0)

    global sun_options, soil_options

    with sqlite3.connect("plantlyfeDB.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Plants WHERE active=1")
        current_plant = c.fetchone()
        print(current_plant)
        if (current_plant != None):
            plantName = current_plant[0]
            plantInfo = (sun_options[current_plant[2]], soil_options[current_plant[3]], current_plant[4], current_plant[5])
            plantMeasurement = (current_plant[1], soil, temperature, humidity, light_needs, water_level)
            log_measurement(soil, temperature, humidity, light_needs, water_level)
        else:
            plantName = "No current plant"
            plantInfo = None
            plantMeasurement = (0, soil, temperature, humidity, light_needs, water_level)
        
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
        # timeStamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
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
    return redirect("/")

# @app.route("/logout")
# def logout():

def log_measurement(soil, humidity, temperature, water_level, light_needs):
    with sqlite3.connect("plantlyfeDB.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Plants WHERE active=1")
        current_plant = c.fetchone()
        measurement = (current_plant[1], soil, humidity, temperature, water_level, light_needs, time.strftime('%Y-%m-%d %H:%M:%S'))
        c.execute("INSERT INTO PlantMeasurements VALUES (?, ?, ?, ?, ?, ?, ?)", measurement)
        conn.commit()

# TO DO: Create database with users, users plants, and plant data
# TO DO: When loading home, update values reading from "sensors"
# TO DO: Log sensor data to database, periodically (x times daily)
# TO DO: Add plant feature
# TO DO: Login feature
def take_measurements(sleep_time):
    global soil, humidity, temperature, water_level, light_needs
    while True:
        soil  = round(getSoilReading(), 2)
        humidity, temperature = getHumidityTemperatureReading()
        temperature = round(temperature, 2)
        humidity = round(humidity, 2)
        water_level, light_needs = getFSRandPRreading()
        time.sleep(sleep_time)
        
if __name__ == "__main__":
    t1 = Thread(target=take_measurements, args=[1])
    t1.start()
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
    t1.join()



# t1 = Thread(target=take_measurements, args=[60000])
# t1.start()
# t1.join()
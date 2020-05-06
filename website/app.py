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

device_id = 1

@app.route("/")
def home():
    # Do some operations to find these values
    # take_measurements(0)
    with sqlite3.connect("plantlyfeDB.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Plants")
        current_plant = c.fetchone()
        print(current_plant)
        if (current_plant != None):
            plantName = current_plant[0]
        else:
            plantName = "No current plant"
        plantMeasurement = (soil, temperature, humidity, light_needs, water_level)
    return render_template('index.html', plantName=plantName, plantData=plantMeasurement, plantNeeds=current_plant)

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
            # c.execute("UPDATE Plants SET active=FALSE WHERE active=TRUE")

            entry = (plantName, plantID, sunlight, soilMoisture, lowestTemp, highestTemp, "TRUE")
            c.execute("INSERT INTO Plants VALUES (?, ?, ?, ?, ?, ?, ?)", entry)
            conn.commit()
    else:
        print("NO REQUEST")
    return redirect("/")

@app.route("/editplant")
def editplant():
    with sqlite3.connect("plantlyfeDB.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Plants")
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
# @app.route("/logout")
# def logout():

# TO DO: Create database with users, users plants, and plant data
# TO DO: When loading home, update values reading from "sensors"
# TO DO: Log sensor data to database, periodically (x times daily)
# TO DO: Add plant feature
# TO DO: Login feature
def take_measurements(sleep_time):
    global soil, humidity, temperature, water_level, light_needs, device_id
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
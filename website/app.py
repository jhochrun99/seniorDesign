from flask import Flask, redirect, render_template
from threading import Thread
from plantLyfe import *
import time

app = Flask(__name__, static_folder='')

soil = 0
temperature = 0
humidity = 0
light_needs = 0
water_level = 0

@app.route("/")
def home():
    # Do some operations to find these values
    # take_measurements(0)
    return render_template('index.html', soil=soil, temp=temperature, hum=humidity, light=light_needs, water=water_level)

# @app.route("/addplant")
# def addplant():

# @app.route("/logout")
# def logout():

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
        # updateDatabase()
        time.sleep(sleep_time)
        
if __name__ == "__main__":
    t1 = Thread(target=take_measurements, args=[1])
    t1.start()
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
    t1.join()



# t1 = Thread(target=take_measurements, args=[60000])
# t1.start()
# t1.join()
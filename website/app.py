from flask import Flask, redirect, render_template

app = Flask(__name__, static_folder='')

@app.route("/")
def home():
    # Do some operations to find these values
    soil = "Damp"
    temperature = 79
    humidity = 43
    light_needs = 85
    water_level = "Low"
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

# if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
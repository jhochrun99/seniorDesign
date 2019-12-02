import Adafruit_DHT

DHT_PIN = 4
sensor = Adafruit_DHT.DHT11

while(1):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        print("Failed to read.")
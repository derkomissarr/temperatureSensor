import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import board
import busio
import digitalio

import adafruit_max31865

# Initialize SPI bus and sensor.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)  # Chip select of the MAX31865 board.
#sensor = adafruit_max31865.MAX31865(spi, cs)
# Note you can optionally provide the thermocouple RTD nominal, the reference
# resistance, and the number of wires for the sensor (2 the default, 3, or 4)
# with keyword args:
sensor = adafruit_max31865.MAX31865(spi, cs, rtd_nominal=100, ref_resistor=425.5, wires=2)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.

client = mqtt.Client()
client.on_connect = on_connect
client.connect("192.168.1.251", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.


while 0 == client.loop():
    # Read temperature.
    temp = (sensor.temperature-0.2)
    # Print the value.
    print('Temperature: {0:0.3f}C'.format(temp))
    # Delay for a second.
    publish.single("temp/", payload='{0:0.3f}'.format(temp), client_id="Wohnzimmer")
    time.sleep(101.0)

client.loop_forever()






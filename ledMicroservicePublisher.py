import paho.mqtt.publish as publish
import json
import time
import sys

start = time.time()
MQTT_SERVER = sys.argv[1]
MQTT_PATH = "LED"

pi_file = open("DataModelPi.json", "r")  # open the file in read-only mode
pi_model = json.load(pi_file)  # cßonvert file object to json object
pi_file.close()

count = 0

while count < 20:
    try:
        pi_file = open("DataModelPi.json", "w")  # open the file in write mode
        led_1_value = pi_model["pi"]["actuators"]["leds"]["1"]["value"] # get led 1 current value
        led_1_gpio = pi_model["pi"]["actuators"]["leds"]["1"]["gpio"] # get led 1 gpio
        pi_model["pi"]["actuators"]["leds"]["1"]["value"] = not led_1_value  # negate led1 value data model
        json.dump(pi_model, pi_file, indent=2)  # overwrite previous data model
        pi_file.close()

        temp_json = {"LED_1": not led_1_value, "GPIO": led_1_gpio} #create json message that will be sent
        publish.single(MQTT_PATH, json.dumps(temp_json), port=1883, hostname=MQTT_SERVER)

    except RuntimeError as error:  # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
    count += 1
    time.sleep(1)
publish.single(MQTT_PATH, json.dumps({"Done": True}), port=1883, hostname=MQTT_SERVER)
end = time.time()
print("led publisher runtime: " + str(end-start))
with open("macResults.txt", "a") as myfile:
    myfile.write("LED publisher runtime = " + str(end-start) + "\n")

import paho.mqtt.client as mqtt
import json
import sys
import time

start = time.time()
MQTT_SERVER = sys.argv[1] #ip address of raspberry pi. needed for MQTT broker
MQTT_PATH = "Humidity"

#the following code runs upon connecting
def on_connect(client, userdata, flags, rc):
    print("Connected. Result code: " + str(rc))
    client.subscribe(MQTT_PATH)

#the on_message function runs once a message is received from the broker
def on_message(client, userdata, msg):
    received_json = json.loads(msg.payload) #convert the string to json object
    if "Done" in received_json:
        client.loop_stop()
        client.disconnect()
        end = time.time()
        timer = end-start
        print("Humidity subscriber closing. Runtime: " + str(timer))
        with open("macResults.txt", "a") as myfile:
            myfile.write("Humidity subscriber runtime = " + str(timer) + "\n")
    else:
        pi_file = open("PiDataModel.json", "r") #open the file in read-only mode
        pi_model = json.load(pi_file) #convert file object to json object
        pi_file.close()

        pi_file = open("PiDataModel.json", "w") #open the file in write mode
        if pi_model["pi"]["sensors"]["humidity"]["value"] != received_json["Humidity"]:
            pi_model["pi"]["sensors"]["humidity"]["value"] = received_json["Humidity"] #change data model
            json.dump(pi_model, pi_file, indent=2) #overwrite previous data model
        pi_file.close()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60) #ip, port and...
client.loop_forever() #continue waiting for messages
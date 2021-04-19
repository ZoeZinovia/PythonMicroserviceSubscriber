import paho.mqtt.client as mqtt
import json
import sys
import time

start = time.time()

MQTT_SERVER = sys.argv[1]
MQTT_PATH = "PIR"

def on_connect(client, userdata, flags, rc):
    print("Connected. Result code: "+ str(rc))
    client.subscribe(MQTT_PATH)


#the on_message function runs once a message is received from the broker
def on_message(client, userdata, msg):
    received_json = json.loads(msg.payload) #convert the string to json object
    if "Done" in received_json:
        client.loop_stop()
        client.disconnect()
        end = time.time()
        timer = end-start
        print("PIR subscriber closing. Runtime: " + str(timer))
        with open("macResults.txt", "a") as myfile:
            myfile.write("PIR subscriber runtime = " + str(timer) + "\n")
    else:
        pi_file = open("PiDataModel.json", "r") #open the file in read-only mode
        pi_model = json.load(pi_file) #convert file object to json object
        pi_file.close()

        if pi_model["pi"]["sensors"]["pir"]["value"] != received_json["PIR"] == 1:
            pi_file = open("PiDataModel.json", "w")  # open the file in write mode
            pi_model["pi"]["sensors"]["pir"]["value"] = received_json["PIR"] == 1 #change data model
            json.dump(pi_model, pi_file, indent=2) #overwrite previous data model
            pi_file.close()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)
client.loop_forever()
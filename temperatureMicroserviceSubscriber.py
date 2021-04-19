import paho.mqtt.client as mqtt
import json
import sys
import time

start = time.time()
MQTT_SERVER = sys.argv[1]
MQTT_PATH = "Temperature"

def on_connect(client, userdata, flags, rc):
    print("Connected. Result code: "+ str(rc))
    client.subscribe(MQTT_PATH)


#the on_message function runs once a message is received from the broker
def on_message(client, userdata, msg):
    # msg.payload = msg.payload.decode("utf-8")
    # global timer
    print("message received: " + str(msg.payload))
    received_json = json.loads(msg.payload) #convert the string to json object
    if "Done" in received_json:
        client.loop_stop()
        client.disconnect()
        end = time.time()
        timer = end-start
        print("Temperature subscriber closing. Runtime: " + str(timer))
        with open("macResults.txt", "a") as myfile:
            myfile.write("Temperature subscriber runtime = " + str(timer) + "\n")
        print("updated runtime file")
    else:
        pi_file = open("PiDataModel.json", "r") #open the file in read-only mode
        pi_model = json.load(pi_file) #cßonvert file object to json object
        pi_file.close()

        pi_file = open("PiDataModel.json", "w") #open the file in write mode
        pi_model["pi"]["sensors"]["temperature"]["value"] = received_json["Temp"] #change data model
        json.dump(pi_model, pi_file, indent=2) #overwrite previous data model
        pi_file.close()
        print("JSON temperature data model updated")
        # end = time.time()
        # timer = timer + (end - start)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)
client.loop_forever()
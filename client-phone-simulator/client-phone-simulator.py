from datetime import datetime
import paho.mqtt.client as mqtt 
import time, sys

broker_hostname = "localhost"
port = 1883 

def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("connected")
    else:
        print("could not connect, return code:", return_code)

client = mqtt.Client("Client1")
client.on_connect=on_connect

client.connect(broker_hostname, port)
client.loop_start()

topic = "idc/FC56323"

with open("online.data", "r") as file:
    msg = [line.rstrip() for line in file]

msg = msg[1:]

msg_count = 0
while True:
    try:
        time.sleep(1)
        current_msg = datetime.now().strftime("%d/%m/%y;%H:%M:%S:000000000;") + msg[msg_count]
        result = client.publish(topic, current_msg)
        status = result[0]
        if status == 0:
           print("Message "+ current_msg + " is published to topic " + topic)
        else:
           print("Failed to send message to topic " + topic)
        msg_count = (msg_count + 1) % len(msg)
    except KeyboardInterrupt:
        print("Shuting down")
        client.loop_stop()
        sys.exit()
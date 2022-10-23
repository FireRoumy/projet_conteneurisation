# python 3.6

import random
from time import sleep
import csv

from paho.mqtt import client as mqtt_client


broker = "mosquitto"
port = 1883
topic = "mqtt/data"
# generate client ID with pub prefix randomly
client_id = "MQTTPublisher"
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    while(1):
        for i in range(3, 12):            
            stringToSend = ""
            randomsleep = random.randint(2, 10)
            sleep(randomsleep)
            #sleep(10)
            with open('Eau_Potable_Barnier.csv', mode='r', encoding = "ISO-8859-1") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter = ';')                 
                line_count = 0   
                for row in csv_reader:
                    if(line_count == 0 or line_count == 16 or line_count == 17 or line_count == 18 or line_count == 19 or line_count == 20 or line_count == 21):
                        #print(line_count, "//////", row[i])
                        stringToSend += row[i] + ";"
                    line_count += 1                 
            print(stringToSend)
            result = client.publish(topic, stringToSend)  # publish
            status = result[0]
            if status == 0:
                print(f"Send `{stringToSend}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
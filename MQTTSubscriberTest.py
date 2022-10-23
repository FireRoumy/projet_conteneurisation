#MQTT
import random
from paho.mqtt import client as mqtt_client
from datetime import datetime
#InfluxDB
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS

#MQTT
broker = "44.201.92.7"
port = 1883
topic = "mqtt/data"
# generate client ID with pub prefix randomly
client_id = "MQTTSubscriber"
# username = 'emqx'
# password = 'public'
#InfluxDB
token = "bmDLXMwdrf95qc8mMhoTm-nZLcDnYNge-j7vRWgicWHFAC5Rz4dGfhWEr6_B8hFATArCyvtJ3JQespdURJ8Psg=="
#token = "'wj8KipGh40m2xEjO4bQwTV50QjXGLX-A592NeBQ5ETHOs6vMnI-WXXmtEUkP32iRfcXRhxMcmAvD2QNoCmdoYQ=='"
org = "grandlyon"
bucket = "grandlyon-data"

#InfluxDB
class InfluxClient:
    def __init__(self,token,org,bucket): 
        self._org=org 
        self._bucket = bucket
        self._client = InfluxDBClient(url="http://http://44.201.92.7:8086", token=token)

    def write_data(self,data,write_option=SYNCHRONOUS):
        write_api = self._client.write_api(write_option)
        write_api.write(self._bucket, self._org , data,write_precision='s')

#MQTT
def connect_mqtt() -> mqtt_client:
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


def subscribe(client: mqtt_client, IC: InfluxClient):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        processAndWriteDB(IC, msg.payload.decode())

    client.subscribe(topic)
    client.on_message = on_message


def run(IC: InfluxClient):
    client = connect_mqtt()
    subscribe(client, IC)
    client.loop_forever()

def processAndWriteDB(IC: InfluxClient, dataReceived):

    dataReceivedClean = dataReceived.replace(" ","")
    dataReceivedSplit = dataReceivedClean.split(";")
    #volumes_produits = dataReceivedSplit[1] + "(" + dataReceivedSplit[0] + ")"
    #volumes_achetes = dataReceivedSplit[2] + "(" + dataReceivedSplit[0] + ")"
    #volumes_vendus = dataReceivedSplit[3] + "(" + dataReceivedSplit[0] + ")"
    #volumes_introduits = dataReceivedSplit[4] + "(" + dataReceivedSplit[0] + ")"
    #volumes_consommes = dataReceivedSplit[5] + "(" + dataReceivedSplit[0] + ")"
    #volumes_perdus = dataReceivedSplit[6] + "(" + dataReceivedSplit[0] + ")"
    
    #dataToSend = f"consommation_eau,produit=eau volumes_produits={volumes_produits},volumes_achetes={volumes_achetes},volumes_vendus={volumes_vendus},volumes_introduits={volumes_introduits},volumes_consommes={volumes_consommes},volumes_perdus={volumes_perdus}"
    #IC.write_data([dataToSend])

    dataToSend = f"consommation_eau,produit=eau volumes_produits={dataReceivedSplit[1]},volumes_achetes={dataReceivedSplit[2]},volumes_vendus={dataReceivedSplit[3]},volumes_introduits={dataReceivedSplit[4]},volumes_consommes={dataReceivedSplit[5]},volumes_perdus={dataReceivedSplit[6]}"
    IC.write_data([dataToSend])
    print(f"Write `{dataToSend}` in InfluxDB on {IC._bucket}")
    #dataToSend = f"consommation_eau,annee={dataReceivedSplit[0]} volumes_produits={dataReceivedSplit[1]}"
    #IC.write_data([dataToSend])
    #dataToSend = f"consommation_eau,annee={dataReceivedSplit[0]} volumes_achetes={dataReceivedSplit[2]}"
    #IC.write_data([dataToSend])
    #dataToSend = f"consommation_eau,annee={dataReceivedSplit[0]} volumes_vendus={dataReceivedSplit[3]}"
    #IC.write_data([dataToSend])
    #dataToSend = f"consommation_eau,annee={dataReceivedSplit[0]} volumes_introduits={dataReceivedSplit[4]}"
    #IC.write_data([dataToSend])
    #dataToSend = f"consommation_eau,annee={dataReceivedSplit[0]} volumes_consommes={dataReceivedSplit[5]}"
    #IC.write_data([dataToSend])
    #dataToSend = f"consommation_eau,annee={dataReceivedSplit[0]} volumes_perdus={dataReceivedSplit[6]}"
    #IC.write_data([dataToSend])

if __name__ == '__main__':
    IC = InfluxClient(token,org,bucket)
    run(IC)    
    

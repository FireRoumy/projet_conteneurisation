import paho.mqtt.client as mqtt

broker = "127.0.0.1"
port = 1883
topic = "data"

def on_connect(client, userdata, flags, rc):  # The callback for when 
    #the client connects to the broker 
    print("Connected with result code {0}".format(str(rc)))  
    # Print result of connection attempt client.subscribe("digitest/test1")  
    # Subscribe to the topic “digitest/test1”, receive any messages 
    #published on it

def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")   

client = mqtt.Client("CsvPublish")  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message
#client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
client.connect(broker, port) 
client.subscribe(topic)
client.loop_forever()  # Start networking daemon


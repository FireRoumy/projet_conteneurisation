import csv
from time import sleep
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

def on_publish(client, userdata, result):  # create function for callback
    pass

client = mqtt.Client("CsvPublish")  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_publish = on_publish  # assign function to callback
#client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
client.connect(broker, port) 
#client.loop_start()
#client.loop_forever()  # Start networking daemon

while(1):
    for i in range(3, 12):
        
        stringToSend = ""
        sleep(5)

        with open('Eau_Potable_Barnier.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ';')                 
            line_count = 0   
            for row in csv_reader:
                if(line_count == 0 or line_count == 16 or line_count == 17 or line_count == 18 or line_count == 19 or line_count == 20
                | line_count == 21 or line_count == 22):
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
    
        
   

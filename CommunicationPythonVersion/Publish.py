import machine
import network
from umqtt.simple import MQTTClient
import json


def do_publish(mqtt_config, topics_dict):
    #Preparing mqtt client object
    client = MQTTClient(mqtt_config["client_id"],
                        mqtt_config["host"], 
                        mqtt_config["port"],
                        mqtt_config["user"],
                        mqtt_config["password"])
    try:
        client.connect():
    except Exception as e:
            print("MQTT connection failed due to: ", e)
            return -1
    
    #Get device MAC address in form of aabbccdd
    mac = machine.unique_id()
    MAC = ''.join('{:02x}'.format(b) for b in ) 
    
    #Publish topics to a server.
    try:
        for topic,json in topics_dict:
            payload = json.dumps(json)
            client.publish(MAC + "/"+topic, payload) 
    except Exception as e:
                print(" Error publishing:", e)
    client.disconnect()
    return 1


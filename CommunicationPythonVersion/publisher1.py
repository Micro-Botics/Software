import time
import ubinascii
import machine
import json
from umqtt.simple import MQTTClient

# MQTT Broker details
MQTT_BROKER = "test.mosquitto.org"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"temperature"

# Callback function triggered on message
def sub_cb(topic, msg):
    print("Received:", topic, msg)

def connect_mqtt():
    """Try to connect repeatedly until successful."""
    while True:
        try:
            print("Attempting MQTT connection...")
            client = MQTTClient(
                client_id=CLIENT_ID,
                server=MQTT_BROKER,
                keepalive=60
            )
            client.set_callback(sub_cb)
            client.connect()
            print("Connected successfully.")
            return client

        except Exception as e:
            print("MQTT connection failed:", e)
            print("Retrying in 5 seconds...")
            time.sleep(5)

def do_publish(client, topic, json_data):
    """
    Publica un diccionario JSON en un topic MQTT.
    """
    try:
        payload = json.dumps(json_data)
        client.publish(topic, payload)
        print(" Published to", topic, ":", payload)

    except Exception as e:
        print(" Error publishing:", e)


def main():
    mqttClient = connect_mqtt()

    # Ejemplo: si quieres suscribirte también
    mqttClient.subscribe(TOPIC)
    print("Subscribed to topic:", TOPIC)

    try:
        while True:
            # Aquí publicas lo que quieras (cada X segundos)
            data = {
                "temperature": 25.4,
                "humidity": 58,
                "device": CLIENT_ID.decode()
            }

            publish(mqttClient, TOPIC, data)
            time.sleep(5)

    except KeyboardInterrupt:
        print("Disconnecting...")
        mqttClient.disconnect()


if __name__ == "__main__":
    main()

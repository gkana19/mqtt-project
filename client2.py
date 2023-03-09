import random
import time
import pandas as pd
import uuid
from paho.mqtt import client as mqtt_client
import socket


# Get IP address of current machine
IP_ADDRESS = socket.gethostbyname(socket.gethostname())

# Define maximum packet size for MQTT messages
MAX_PACKET_SIZE = 250

# Define MQTT broker settings
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "cpenetworklab1/2048"

# Generate client ID with pub prefix randomly
CLIENT_ID = f"python-mqtt-{random.randint(0, 1000)}"

# Set MQTT username and password
USERNAME = "emqx"
PASSWORD = "public"

flag_connected = 0


def connect_mqtt():

    # Create new MQTT client instance
    client = mqtt_client.Client(CLIENT_ID)

    # Set MQTT username and password
    client.username_pw_set(USERNAME, PASSWORD)

    # Set MQTT connection handler
    client.on_connect = on_connect

    # Connect to MQTT broker
    client.connect(BROKER, PORT)
    # print("Connect flag:", flag_connected)

    return client

# Define MQTT connection handler


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        global flag_connected
        flag_connected = 1
        # Send connected flags to subscribe
        client.publish(TOPIC, f"{flag_connected} {IP_ADDRESS}")  # ==> 1
        print("Connected to MQTT Broker! from", IP_ADDRESS)
    else:
        print("Failed to connect, return code %d\n", rc)


def on_disconnect(client, userdata, rc):
    # Define handler for MQTT disconnection
    if rc != 0:
        print("Unexpected to Disconnect, return code %d\n", rc)
    else:
        global flag_connected
        flag_connected = 0
        print("Disconnect Success", rc)


def read_sensor_data():
    # Read sensor data from Excel file using pandas library
    df = pd.read_excel("SampleInput.xlsx")
    return df.to_dict("records")


def publish(client):
    # Get sensor data as a list of dictionaries
    sensor_data = read_sensor_data()

    # Loop through sensor data and publish to MQTT broker
    for i, data in enumerate(sensor_data):
        # Generate unique ID for data packet
        data_id = str(uuid.uuid4())
        time.sleep(0.5)

        # Convert data dictionary to string
        msg = str(data)

        # Split message into multiple packets if larger than maximum packet size
        packets = [
            msg[i: i + MAX_PACKET_SIZE] for i in range(0, len(msg), MAX_PACKET_SIZE)
        ]

        # Publish packets to MQTT broker
        for j, packet in enumerate(packets):
            time.sleep(0.3)
            result = client.publish(
                TOPIC, f"{IP_ADDRESS}, {data_id}, {j}, {packet}")
            status = result[0]
            if status == 0:
                print(f"Sent {packet} to topic {TOPIC} ({i}, {j})")
                # print(f"send {data_id} to topic {TOPIC} ({i}, {j})")
            else:
                print(f"Failed to send message to topic {TOPIC}")

        # Publish end-of-packet marker to MQTT broker
        time.sleep(0.5)
        client.publish(TOPIC, f"{IP_ADDRESS}, {data_id}, -1, end")
        print("Wait-time 3 minute")
        time.sleep(10)  # Wait for 3 minute to send a new message
    # Publish end-of-data marker to MQTT broker
    time.sleep(0.5)
    client.publish(TOPIC, f"0 {IP_ADDRESS}")


def run():
    # Connect to MQTT broker and publish sensor data
    client = connect_mqtt()
    client.loop_start()
    try:
        publish(client)
    except KeyboardInterrupt:
        # Sent flag 0 to subscriber
        client.publish(TOPIC, f"0 {IP_ADDRESS}")
        print("KeyBoardInterrupt")

    # Set MQTT disconnection handler and disconnect from broker
    client.on_disconnect = on_disconnect
    client.disconnect()
    client.loop_stop()


if __name__ == "__main__":
    run()

"""
Test client
"""

import paho.mqtt.client as mqtt

SERVER = "50b39c42c0ce4e079d9694e03cf5b2c6.s1.eu.hivemq.cloud"
PORT = 8883


# The callback for when the client receives a CONNACK response from the server.
def on_connect(_client, userdata, flags: dict, rc: str, properties=None):
    print(f"Connected with result code: {rc}, flags: {flags['session present']}")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    _client.subscribe("/test-home/#")


def on_disconnect(_client, userdata, rc, properties=None):
    print(f"USERDATA: {userdata}, RC: {rc}")


# The callback for when a PUBLISH message is received from the server.
def on_message(_client, userdata, msg):
    print(f"MESSAGE TOPIC={msg.topic}",
          f"- PAYLOAD={str(msg.payload)}",
          f"- QOS={msg.qos}",
          f"- RETAIN={msg.retain}")


client = mqtt.Client(client_id="666",
                     userdata=None,
                     protocol=mqtt.MQTTv5,
                     transport="tcp")
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set("stepan", "1q2w3E4R")

client.connect(host=SERVER,
               port=PORT,
               keepalive=60)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()
client.loop_forever(timeout=1.0)

"""
Test client
"""

import paho.mqtt.client as mqtt
import logging
import argparse
import json
from json import JSONDecodeError


def main():
    parser = argparse.ArgumentParser(prog="MQTT Client",
                                     usage="client.py [operator]",
                                     description="Test client for MQTT",
                                     epilog="Part of the Apollo core",
                                     prefix_chars='-',
                                     add_help=True)
    parser.add_argument("--websocket",
                        action='store_true',
                        default=False,
                        help="Try connect via websocket")
    arguments = parser.parse_args()

    logging.basicConfig(filename="client.log",
                        filemode='a',
                        level=logging.NOTSET)
    logger = logging.getLogger(__name__)

    SERVER = "50b39c42c0ce4e079d9694e03cf5b2c6.s1.eu.hivemq.cloud"

    if arguments.websocket:
        PORT = 8884
        SOCKET = "websockets"
    else:
        PORT = 8883
        SOCKET = "tcp"

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(_client, userdata, flags: dict, rc: str, properties=None):
        print(f"Connect established with code: {rc}, across {SOCKET}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        _client.subscribe("/test-home/#", 0)

    def on_disconnect(_client, userdata, rc, properties=None):
        print(f"Connect broken with code: {rc}, userdata {userdata}")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(_client, userdata, msg):
        try:
            payload = json.loads(msg.payload)
        except JSONDecodeError:
            payload = msg.payload

        print(f"MESSAGE RECIEVED: TOPIC={msg.topic}, ",
              f"PAYLOAD={payload}, ",
              f"QOS={msg.qos}, ",
              f"RETAIN={msg.retain}, "
              f"USERDATA={userdata}")
        print("===================================")

    client = mqtt.Client(client_id="67567567567567",
                         userdata=None,
                         protocol=mqtt.MQTTv311,
                         transport=SOCKET)
    client.enable_logger(logger)
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    client.username_pw_set("stepan", "1q2w3E4R")

    client.connect(host=SERVER,
                   port=PORT,
                   keepalive=60,
                   clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.loop_forever(timeout=1.0)


if __name__ == "__main__":
    main()

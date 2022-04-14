"""
Test publisher
"""

import paho.mqtt.publish as pub
import paho.mqtt.client as mqtt
import json
import argparse
import logging


class ArgRead:
    websocket = False


parser = argparse.ArgumentParser(description="Test publisher for MQTT")
parser.add_argument("--websocket", action='store_true')
parser.parse_args(args=['--websocket'],
                  namespace=ArgRead)

logging.basicConfig(filename="pub.log",
                    filemode='a',
                    level=logging.NOTSET)
logger = logging.getLogger(__name__)

SERVER = "50b39c42c0ce4e079d9694e03cf5b2c6.s1.eu.hivemq.cloud"

PTEST = {"uuid": "888",
         "type": "test",
         "bool": True,
         "null": None}

AUTH = {"username": "stepan", "password": "1q2w3E4R"}
TLS = {"tls_version": mqtt.ssl.PROTOCOL_TLS}

if ArgRead.websocket:
    PORT = 8884
    SOCKET = "websockets"
else:
    PORT = 8883
    SOCKET = "tcp"

try:
    pub.single("/test-home/message",
               payload=json.dumps(PTEST),
               qos=2,
               retain=True,
               hostname=SERVER,
               port=PORT,
               client_id="",
               auth=AUTH,
               tls=TLS,
               protocol=mqtt.MQTTv311,
               transport=SOCKET)
    pub.single("/test-home/callback",
               payload="TEST18",
               qos=2,
               retain=False,
               hostname=SERVER,
               port=PORT,
               client_id="",
               auth=AUTH,
               tls=TLS,
               protocol=mqtt.MQTTv311,
               transport=SOCKET)
except Exception as err:
    print(f"Message not sent, because {err}")
else:
    print(f"All message sent, across {SOCKET}")

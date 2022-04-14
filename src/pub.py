"""
Test publisher
"""

import paho.mqtt.publish as pub
import paho.mqtt.client as mqtt
import json

SERVER = "50b39c42c0ce4e079d9694e03cf5b2c6.s1.eu.hivemq.cloud"
PORT = 8883

PTEST = {"uuid": "888",
         "type": "test",
         "bool": True,
         "null": None}

AUTH = {"username": "stepan", "password": "1q2w3E4R"}
TLS = {"tls_version": mqtt.ssl.PROTOCOL_TLS}

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
               transport="tcp")
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
               transport="tcp")
except Exception as err:
    print(f"Message not sent, because {err}")
else:
    print("all message sent")

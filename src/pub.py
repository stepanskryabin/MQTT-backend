"""
Test publisher
"""

import paho.mqtt.publish as pub
import paho.mqtt.client as mqtt

SERVER = "50b39c42c0ce4e079d9694e03cf5b2c6.s1.eu.hivemq.cloud"
PORT = 8883

AUTH = {"username": "stepan", "password": "1q2w3E4R"}
TLS = {"tls_version": mqtt.ssl.PROTOCOL_TLS}

pub.single("/test-home/message",
           payload="test4",
           qos=0,
           retain=True,
           hostname=SERVER,
           port=PORT,
           client_id="666",
           auth=AUTH,
           tls=TLS,
           protocol=mqtt.MQTTv5,
           transport="tcp")

pub.single("/test-home/callback",
           payload="callback test",
           qos=0,
           retain=True,
           hostname=SERVER,
           port=PORT,
           client_id="666",
           auth=AUTH,
           tls=TLS,
           protocol=mqtt.MQTTv5,
           transport="tcp")

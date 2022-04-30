"""
Test publisher
"""
import random
import time

import paho.mqtt.publish as pub
import paho.mqtt.client as mqtt
import json
import argparse
import logging
import uuid

logging.basicConfig(filename="pub.log",
                    filemode='a',
                    level=logging.NOTSET)
logger = logging.getLogger(__name__)
logger.level = 10

# Config devices
ID = uuid.uuid1()
TYPE = 'channel'
NAME = 'Канал'


# Config MQTT broker
SERVER = "50b39c42c0ce4e079d9694e03cf5b2c6.s1.eu.hivemq.cloud"
AUTH = {"username": "stepan",
        "password": "1q2w3E4R"}
TLS = {"tls_version": mqtt.ssl.PROTOCOL_TLS}


def description(publisher_type: str = 'button',
                publisher_name: str = 'Кнопка в холле'):
    return {'type': publisher_type,
            'name': publisher_name}


def state_control(value=0.0):
    return {"value": value}


def config(raise_time=0.0,
           fall_time=0.0,
           sacn_universe=random.randrange(1, 63999, 1),
           sacn_priority=100,
           sacn_name="APOLLO",
           sacn_pps=0):
    return {"raise_time": raise_time,
            "fall_time": fall_time,
            "sacn_universe": sacn_universe,
            "sacn_priority": sacn_priority,
            "sacn_name": sacn_name,
            "sacn_pps": sacn_pps}


def main(server: str,
         auth: dict,
         tls: dict):
    parser = argparse.ArgumentParser(description="Test publisher for MQTT")
    parser.add_argument("--websocket", action='store_true', default=False)
    arguments = parser.parse_args()

    if arguments.websocket:
        PORT = 8884
        SOCKET = "websockets"
    else:
        PORT = 8883
        SOCKET = "tcp"

    try:
        pub.single(f"/{ID}/desc",
                   payload=json.dumps(description(TYPE, NAME)),
                   qos=2,
                   retain=False,
                   hostname=server,
                   port=PORT,
                   client_id="",
                   auth=auth,
                   tls=tls,
                   protocol=mqtt.MQTTv5,
                   transport=SOCKET)
        pub.single(f"/{ID}/state",
                   payload=json.dumps(state_control()),
                   qos=2,
                   retain=False,
                   hostname=server,
                   port=PORT,
                   client_id="",
                   auth=auth,
                   tls=tls,
                   protocol=mqtt.MQTTv5,
                   transport=SOCKET)
        pub.single(f"/{ID}/control",
                   payload=json.dumps(state_control()),
                   qos=2,
                   retain=False,
                   hostname=server,
                   port=PORT,
                   client_id="",
                   auth=auth,
                   tls=tls,
                   protocol=mqtt.MQTTv5,
                   transport=SOCKET)
        pub.single(f"/{ID}/config",
                   payload=json.dumps(config()),
                   qos=2,
                   retain=False,
                   hostname=server,
                   port=PORT,
                   client_id="",
                   auth=auth,
                   tls=tls,
                   protocol=mqtt.MQTTv5,
                   transport=SOCKET)
    except Exception as err:
        logger.error(f"Message not sent, because {err}")
    else:
        logger.info(f"All message sent, across {SOCKET}")


if __name__ == "__main__":
    logger.info("Run publisher")
    while True:
        main(SERVER, AUTH, TLS)
        time.sleep(10)

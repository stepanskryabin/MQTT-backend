"""
Test publisher
"""
import random
import time
from typing import List

import paho.mqtt.publish as pub
import paho.mqtt.client as mqtt
import json
import argparse
import logging
import uuid

__version__ = 'v0.1'

LOGGER = {'notset': 0,
          'debug': 10,
          'info': 20,
          'warning': 30,
          'error': 40,
          'critical': 50}

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


def main(connection: bool,
         server: str,
         auth: dict,
         tls: dict):

    if connection:
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
    parser = argparse.ArgumentParser(prog="MQTTPub",
                                     description="Publisher for testing"
                                                 "MQTT connection",
                                     epilog="<stepan.skrjabin@gmail.com>")
    parser.add_argument("--websocket",
                        action='store_true',
                        default=False,
                        help="Establish a prioritized protocol is websocket")
    parser.add_argument("--log",
                        nargs=1,
                        choices=['notset',
                                 'debug',
                                 'info',
                                 'warning',
                                 'error',
                                 'critical'],
                        default='info',
                        help="Config level logging.")
    parser.add_argument("--version",
                        action='version',
                        version=__version__)
    arguments = parser.parse_args()

    logging.basicConfig(filename="pub.log",
                        filemode='a',
                        level=LOGGER[arguments.log])
    logger = logging.getLogger(__name__)

    logger.info("Run publisher")
    logger.info(f"Run with websockets={arguments.websocket}")

    while True:
        main(arguments.websocket,
             SERVER,
             AUTH,
             TLS)
        time.sleep(10)

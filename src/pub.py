"""
Test publisher
"""

import random
import time
import json
import argparse
import logging

import paho.mqtt.publish as pub
import paho.mqtt.client as mqtt

from main_settings import ID, TYPE, NAME, SERVER, AUTH, __version__, \
    LOG_FORMAT, DATE_FORMAT


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
         auth: dict):

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
                   tls={"tls_version": mqtt.ssl.PROTOCOL_TLS},
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
                   tls={"tls_version": mqtt.ssl.PROTOCOL_TLS},
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
                   tls={"tls_version": mqtt.ssl.PROTOCOL_TLS},
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
                   tls={"tls_version": mqtt.ssl.PROTOCOL_TLS},
                   protocol=mqtt.MQTTv5,
                   transport=SOCKET)
    except Exception as err:
        logger.error(f"Message not sent, because {err}")
    else:
        logger.info(f"All message sent, across {SOCKET}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="MQTTPub",
                                     usage='pub.py [--key] [value]',
                                     description="Publisher for testing"
                                                 "MQTT connection",
                                     epilog="<stepan.skrjabin@gmail.com>")
    parser.add_argument("--websocket",
                        action='store_true',
                        default=False,
                        help="establish a prioritized protocol is websocket")
    parser.add_argument("--log",
                        nargs=1,
                        choices=range(0, 60, 10),
                        help="config level logging. \n"
                        "Where 0 - notset, 10 - debug, 20 - info,"
                        "30 - warning, 40 - error, 50 - critical")
    parser.add_argument("--version",
                        action='version',
                        version=__version__)
    arguments = parser.parse_args()

    logging.basicConfig(filename="pub.log",
                        filemode='a',
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT,
                        level=arguments.log[0])
    logger = logging.getLogger(__name__)

    logger.info("Run publisher")
    logger.info(f"Run with websockets={arguments.websocket}")

    while True:
        main(arguments.websocket,
             SERVER,
             AUTH)
        time.sleep(10)

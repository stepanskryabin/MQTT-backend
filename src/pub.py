"""
Test publisher
"""


import random
import json
import uuid
import argparse
import logging

import paho.mqtt.publish as pub
import paho.mqtt.client as mqtt

from main_settings import SERVER, __version__, LOG_FORMAT, DATE_FORMAT

ID1 = uuid.uuid4()
ID2 = uuid.uuid4()


def description(publisher_type: str = 'button',
                publisher_name: str = 'Кнопка в холле'):
    return {'type': publisher_type,
            'name': publisher_name}


def state(locked=False,
          page=None):
    return {"locked": locked,
            "page": page}


def control(lock=False,
            screen_off=None,
            set_page=''):
    return {"lock": lock,
            "screen_off": screen_off,
            "set_page": set_page}


def page(raise_time=0.0,
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
         username: str,
         password: str) -> None:

         qos = 0
         retain = False
         _message = [{"topic": f"/{ID1}/desc",
                     "payload": json.dumps(description('panel', 'СП1')),
                     "qos": qos,
                     "retain": retain},
#                     {"topic": f"/{ID1}/state",
#                     "payload": json.dumps(state(True, "111-222-333")),
#                     "qos": qos,
#                     "retain": retain},
                     {"topic": f"/{ID2}/desc",
                     "payload": json.dumps(description('panel', 'СП2')),
                     "qos": qos,
                     "retain": retain}#,
#                     {"topic": f"/{ID2}/state",
#                     "payload": json.dumps(state(False, "222-333-444")),
#                     "qos": qos,
#                     "retain": retain}
                        ]
         try:
            pub.multiple(msgs=_message,
                         hostname=server,
                         port=8883,
                         auth={'username': username,
                               'password': password},
                         tls={"tls_version": mqtt.ssl.PROTOCOL_TLS},
                         protocol=mqtt.MQTTv5,
                         transport="tcp")
         except Exception as err:
            logger.error(f"Message not sent, because {err}")
         else:
            logger.info("All message sent, across tcp")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="MQTTPub",
                                     usage='pub.py [--key] [value]',
                                     description="Publisher for testing"
                                                 "MQTT connection",
                                     epilog="<stepan.skrjabin@gmail.com>")
    parser.add_argument("--user",
                        action='store',
                        help="имя для авторизация на брокере")
    parser.add_argument("--password",
                        action='store',
                        help="пароль для авторизация на брокере")
    parser.add_argument("--log",
                        nargs=1,
                        type=int,
                        choices=range(0, 60, 10),
                        default=0,
                        help="config level logging. \n"
                        "Where 0 - notset, 10 - debug, 20 - info,"
                        "30 - warning, 40 - error, 50 - critical")
    parser.add_argument("--version",
                        action='version',
                        version=__version__)
    arguments = parser.parse_args()

    logging.basicConfig(filename="pub.log",
                        filemode='w',
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT,
                        level=arguments.log)
    logger = logging.getLogger(__name__)

    logger.info("Run publisher")


    a = 0
    while a < 1:
        main(server=SERVER,
             username=arguments.user,
             password=arguments.password)
        a = 1

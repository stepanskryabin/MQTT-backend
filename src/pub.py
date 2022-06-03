"""
Test publisher
"""

import time
import random
import json
import uuid
import argparse
import logging

import paho.mqtt.publish as pub
import paho.mqtt.client as mqtt

from main_settings import SERVER, __version__, LOG_FORMAT, DATE_FORMAT


def gen_ouid(device: int,
             object: int,
             index: int = None):
    """
    device Типы устройств
    0 - Сервер с GUI
    1 - Сервер
    2 - Кнопочная панель

    object Тип объекта
    0 - Не присвоен
    1 - Кнопка
    2 - Фейдер
    3 - Канал
    4 - Группа каналов
    5 - Аварийный вход (от пожарной сигнализации)
    6 - Шлюз DMX
    7 - Шлюз CAN
    8 - GUI

    index Индекс
    0 - Не присвоен
    1-65535 - Номер
    """

    timestamp = hex(int(time.time()))
    random1 = hex(random.randint(1, 10000))
    random2 = hex(random.randint(1, 10000))
    _device = str(device)
    _object = str(object)
    index = random.randint(1, 65535) if index is None else index
    return f"{timestamp}-{random1}-{random2}-{_device}-{_object}-{index}"

SUFFIX = "/apollo"

ID1 = gen_ouid(device=2, object=1)
ID2 = gen_ouid(device=1, object=6)
ID3 = gen_ouid(device=1, object=7)
ID4 = gen_ouid(device=0, object=8)
ID5 = gen_ouid(device=0, object=8)


def state_button(event=None):
    return {"event": event}

def state_gui(locked=False):
    return {"locked": locked}

def config_dmx(offser=1,
               raise_time=0.0,
               fall_time=0.0,
               _type="sacn",
               universe=30,
               mode=16,
               order="lsb",
               priority=100,
               name="APOLLO",
               pps=0):
    return {"output":[{"offser": offser,
                      "raise_time": raise_time,
                      "fall_time": fall_time,
                      "_type": _type,
                      "universe": universe,
                      "mode": mode,
                      "order": order}],
            "sacn":{"priority": priority,
                    "name": name,
                    "pps": pps}}

def config_can(adress=None):
    if adress is None:
        adress = "192.168.0.44"

    return {"adress": adress}


def main(server: str,
         username: str,
         password: str) -> None:

         qos = 0
         retain = False
         _message = [{"topic": f"{SUFFIX}/objects/{ID1}/state",
                     "payload": json.dumps(state_button("press")),
                     "qos": qos,
                     "retain": retain},
                     {"topic": f"{SUFFIX}/config/dmx/{ID2}",
                     "payload": json.dumps(config_dmx()),
                     "qos": qos,
                     "retain": retain},
                     {"topic": f"{SUFFIX}/config/can/{ID3}",
                     "payload": json.dumps(config_can()),
                     "qos": qos,
                     "retain": retain},
                     {"topic": f"{SUFFIX}/objects/{ID4}/state",
                     "payload": json.dumps(state_gui(True)),
                     "qos": qos,
                     "retain": retain},
                    {"topic": f"{SUFFIX}/objects/{ID5}/control",
                     "payload": json.dumps(state_gui(True)),
                     "qos": qos,
                     "retain": retain}]
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

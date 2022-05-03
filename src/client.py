"""
Test client
"""

import paho.mqtt.client as mqtt
import logging
import argparse
import json
from json import JSONDecodeError
from main_settings import __client_id__, __version__, SERVER, AUTH, \
    LOG_FORMAT, DATE_FORMAT


def main(connection: bool,
         server: str,
         auth: dict,
         topic: str,
         qos: str):
    def on_connect(_client, userdata, flags: dict, rc: str, properties=None):
        logger.info(f"Connect established with code: {rc}, across {SOCKET}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        _client.subscribe(topic, int(qos))

    def on_disconnect(_client, userdata, rc, properties=None):
        logger.info(f"Connect broken with code: {rc}, userdata {userdata}")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(_client, userdata, msg):
        try:
            payload = json.loads(msg.payload)
        except JSONDecodeError:
            logger.error(f"JSONDecoder error: raw message={msg.payload}")
        else:
            logger.info(f"MESSAGE RECIEVED: TOPIC={msg.topic}, "
                        f"PAYLOAD={payload}, "
                        f"QOS={msg.qos}, "
                        f"RETAIN={msg.retain}, "
                        f"USERDATA={userdata}")

    if connection:
        PORT = 8884
        SOCKET = "websockets"
    else:
        PORT = 8883
        SOCKET = "tcp"

    logger.debug(f"Websocket is {connection}")

    client = mqtt.Client(client_id=__client_id__,
                         userdata=None,
                         protocol=mqtt.MQTTv5,
                         transport=SOCKET)

    client.enable_logger(logger)
    logger.debug('Enable Paho.MQTT logger')

    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    client.username_pw_set(username=auth['username'],
                           password=auth['password'])

    client.connect(host=server,
                   port=PORT,
                   keepalive=60,
                   clean_start=mqtt.MQTT_CLEAN_START_FIRST_ONLY)
    logger.debug(f"Connected to server={server}, port:{PORT} via:{SOCKET} "
                 f"used tls protocol:{mqtt.ssl.PROTOCOL_TLS}")

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.loop_forever(timeout=1.0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="MQTTCli",
                                     usage="client.py [--key] [value]",
                                     description="Client fo testing MQTT"
                                                 " connection",
                                     epilog="<stepan.skrjabin@gmail.com>")
    parser.add_argument("--websocket",
                        action='store_true',
                        default=False,
                        help="Establish a prioritized protocol is websocket")
    parser.add_argument("--log",
                        nargs=1,
                        choices=range(0, 60, 10),
                        help="config level logging. \n"
                        "Where 0 - notset, 10 - debug, 20 - info,"
                        "30 - warning, 40 - error, 50 - critical")
    parser.add_argument("--topic",
                        nargs=1,
                        action='store',
                        default='/#',
                        help="Subscribe to the topic of data publication.")
    parser.add_argument("--qos",
                        nargs=1,
                        choices=[0, 1, 2],
                        default="0",
                        help="Quality of service. See MQTT documentation.")
    parser.add_argument("--version",
                        action='version',
                        version=__version__)
    arguments = parser.parse_args()

    logging.basicConfig(filename="client.log",
                        filemode='a',
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT,
                        level=arguments.log[0])
    logger = logging.getLogger(__name__)

    main(arguments.websocket,
         SERVER,
         AUTH,
         arguments.topic,
         arguments.qos)

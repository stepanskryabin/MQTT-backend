import uuid

__version__ = 'v0.1'
__client_id__ = '123456'

LOGGER = {'notset': 0,
          'debug': 10,
          'info': 20,
          'warning': 30,
          'error': 40,
          'critical': 50}

# Config MQTT broker
SERVER = "50b39c42c0ce4e079d9694e03cf5b2c6.s1.eu.hivemq.cloud"
AUTH = {"username": "stepan",
        "password": "1q2w3E4R"}

# Config devices
ID = uuid.uuid1()
TYPE = 'channel'
NAME = 'Канал'

LOG_FORMAT = "%(asctime)s:%(levelname)s-(%(module)s:%(funcName)s): %(message)s"
DATE_FORMAT = '%Y-%m-%d %I:%M:%S:%p'

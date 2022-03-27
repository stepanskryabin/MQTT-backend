import paho.mqtt.publish as pub

pub.single("/test-home/message",
           payload="test2",
           hostname="test.mosquitto.org",
           client_id="6",
           retain=True)

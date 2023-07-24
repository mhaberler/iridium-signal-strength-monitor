import paho.mqtt.client as mqtt
import os, time, json, arrow
from random import randrange
import logging
logging.basicConfig(level=logging.INFO)


user = os.getenv("MQTT_USER")
password = os.getenv("MQTT_PASS")
broker = os.getenv("MQTT_BROKER")
port = int(os.getenv("MQTT_PORT"))

topic = "iridium"

def on_log(client, userdata, level, buf):
    print("log: ",buf)

mqttc = mqtt.Client(f"FakeSignal-{os.getpid()}")
mqttc.on_log=on_log
mqttc.username_pw_set(user, password)
mqttc.connect(broker, port=port)
mqttc.loop_start()


while True:
    signalStrength = randrange(0, 5)
    ts = arrow.Arrow.fromtimestamp(time.time()).isoformat()
    msg = {"timestamp": ts, "signalQuality":signalStrength}
    pl = json.dumps(msg)
    result = mqttc.publish(topic, payload=pl) #, auth=auth)
    status = result[0]
    if result[0] != 0:
        logging.warning(f"failed to publish {topic=} {signalStrength=}")
    time.sleep(1)

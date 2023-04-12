import random
import threading

from django.core.management.base import BaseCommand
from django.conf import settings

from paho.mqtt import client as mqtt_client


class Command(BaseCommand):

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(f'python-mqtt-{random.randint(0, 10000)}')
        client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
        client.on_connect = on_connect
        client.connect(
            host=settings.MQTT_SERVER,
            port=settings.MQTT_PORT,
            keepalive=settings.MQTT_KEEPALIVE
        )
        return client

    def subscribe(self, client, topic):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        client.subscribe(topic)
        client.on_message = on_message

    def run(self, topic):
        client = self.connect_mqtt()
        self.subscribe(client, topic)
        client.loop_forever()

    def handle(self, *args, **options):
        for item in ["$share/g1/story/#", "$SYS/brokers/+/clients/+/+"]:
            threading.Thread(target=self.run, args=(item,)).start()

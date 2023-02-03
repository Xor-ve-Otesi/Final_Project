import network
import time
import keyboard
import paho.mqtt.client as paho

def on_message(self,topic, message, details = False):
    print(2) 
    if topic =='robot':
        data = message
        if old_data != data:
            print(data)

            old_data = data


def callback(topic,msg):
    topic = topic.decode('utf-8')
    msg = msg.decode('utf-8')
    print(2)
    if topic == 'robot_comm/dir':
        print(1)
    
def connectMQTT():
    client = MQTTClient(client_id=b'xorveotesi',
                        server = b'399ce100582845b88e4faf98d82e6735.s2.eu.hivemq.cloud',
                        port = 0,
                        user= b'picomqtt',
                        password = b'123pico.',
                        keepalive = 7200,
                        ssl = True,
                        ssl_params = {'server_hostname':'399ce100582845b88e4faf98d82e6735.s2.eu.hivemq.cloud'})
    client.connect()
    print(5)
    client.set_callback(callback)
    return client

client = connectMQTT()

def reconnect():
    print('Failed to connect to MQTT Broker. Reconnecting...')
    time.sleep(5)

client.subscribe('robot_comm/dir')

while True:
    pass
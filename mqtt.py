import time
import json
import paho.mqtt.client as mqtt

broker = "broker.hivemq.com"
key = ""

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al Broker")
    else:
        print("Problema de coneccion. Codigo = ", rc)


def on_log(client, userdata, flags, buf):
    print("log: " + buf)


def key(client, userdata, message):
    getkey = json.loads(message.payload.decode("utf-8"))
    key = getkey["key"]
    print(key)


def on_message(client, userdata, message):
    data = json.loads(message.payload.decode("utf-8"))
    print(data)
    #print("Received message '" + str(message.payload) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))
    mqttc.publish("lightbulb-discover/" + data["id"] + "/setup", 'start')
    # time.sleep(2)
    # casa = input('Nombre de la casa? \n')
    # setup = "lightbulb-discover/" + data["id"] + "/setup"
    # print(setup)
    # mqttc.publish(setup, casa)
    # time.sleep(2)
    # habitacion = input('Nombre de la habitacion? \n')
    # mqttc.publish(setup, habitacion)
    # time.sleep(2)
    #
    # mqttc.publish("lightbulb-discover/" + data["id"] + "/help")
    #
    # mqttc.subscribe(casa + "/" + habitacion, 1)
    # mqttc.publish(casa + '/' + habitacion + '/' + data["id"] + '/switch',
    #               '{"key":"c220c47c-edfb-4eb9-8b92-669aceb37aa1","switch":"OFF"}')
    time.sleep(4)
    # mqttc.publish("lightbulb-discover/" + data["id"] + "/setup", 'Cuarto1')
    # time.sleep(2)


mqttc = mqtt.Client()
print("Conectandose al broker: " + broker)
mqttc.connect(broker)
mqttc.on_connect = on_connect
mqttc.on_log = on_log
mqttc.on_message = on_message
# mqttc.message_callback_add("lightbulb-discover/r/*", key)
mqttc.subscribe("lightbulb-discover/#", 0)

mqttc.loop_forever()
#while True:
#    mqttc.publish("CasaCuba/Cuarto1/29cc6a48/switch", '{"key": "c220c47c-edfb-4eb9-8b92-669aceb37aa1","switch":"ON"}')
#    time.sleep(1)
#    mqttc.publish("CasaCuba/Cuarto1/29cc6a48/switch", '{"key": "c220c47c-edfb-4eb9-8b92-669aceb37aa1","switch":"OFF"}')
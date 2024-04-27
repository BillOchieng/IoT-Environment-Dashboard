from machine import Pin, I2C
from time import sleep
from picozero import pico_temp_sensor, pico_led
import network
import bme280
import asyncio
from mqtt_as import MQTTClient, config


ssid = "AC-Devices"
password = "alleghenycollege"
config["user"] = "Bill_IoT"
config["password"] = "Bill_ioT@11"
broker = "23ee2ffd9a224d23a9e4e4c0dcbc110b.s1.eu.hivemq.cloud"  # e.g long_hex_string.s2.eu.hivemq.cloud
config["server"] = broker
config["ssl"] = True
config["ssl_params"] = {"server_hostname": broker}

# initialise I2C
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)


def connectMQTT(config):
    broker = "23ee2ffd9a224d23a9e4e4c0dcbc110b.s1.eu.hivemq.cloud"
    config["user"] = "Bill_IoT"
    config["password"] = "Bill_ioT@11"
    config["ssid"] = ssid
    config["wifi_pw"] = password
    config["port"] = 8883
    config["keepalive"] = 60
    config["server"] = broker
    config["ssl"] = True
    config["ssl_params"] = {"server_hostname": broker}
    return MQTTClient(config)


client = connectMQTT(config)


def publish(topic, value):
    print(topic)
    print(value)
    client.publish(topic, value)
    print("publish Done")


async def main(client):
    await client.connect()
    while True:
        await asyncio.sleep(5)
        sensor_reading = bme280.BME280(i2c=i2c)
        t = pico_temp_sensor.temp
        temp = sensor_reading.values[0]
        pressure = sensor_reading.values[1]
        humidity = sensor_reading.values[2]
        print(temp, t, humidity, pressure)
        await client.publish("temp(p)", "{}".format(t), qos=1)
        await client.publish("temp(s)", "{}".format(temp), qos=1)
        await client.publish("pressure", "{}".format(pressure), qos=1)
        await client.publish("humidity", "{}".format(humidity), qos=1)


MQTTClient.DEBUG = True  # Optional: print diagnostic messages
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors

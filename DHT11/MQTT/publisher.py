import dht
import machine
import network
import time
import random
from umqtt.robust import MQTTClient

#dht11 sensor
d = dht.DHT11(machine.Pin(15))
def read_dht11():
    d.measure()
    temp = d.temperature()
    hum = d.humidity()
    return temp, hum

#connect to WLAN
def connect(ssid, password):
    # ssid =  ssid
    # password = password
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    print(wlan.ifconfig())

#get time from network
def get_time():
    import ntptime
    ntptime.host = 'time.stdtime.gov.tw'
    ntptime.settime()
    # print(time.localtime())

# MQTT setup
def mqtt_setup():
    # You can use your own broker or free public broker
    # broker_ip = "192.168.0.121" #your laptop IP
    broker_ip = "test.mosquitto.org" # use the test MQTT broker
    client = MQTTClient("pico_w_client", broker_ip)
    try:
        client.connect()
        print('Connected to MQTT broker')
    except OSError as e:
        print(f"connection error：{e}")

    return client

#continuous read and publish as json
def main():
    topic = "pico_w_dht11"
    while True:
        temp, hum = read_dht11()
        # temp, hum = random.randint(20, 30), random.randint(40, 60)
        current_time = time.localtime()
        timezone_offset = 8 * 3600
        taiwan_time = time.localtime(time.mktime(current_time) + timezone_offset)
        message = f'{{"CurrentTime":{list(taiwan_time)}, "temperature":{temp}, "humidity":{hum}}}'
        client.publish(topic, message)
        print(f"Published: {message}")
        time.sleep(5)

try:
    connect('ssid', 'password')
    get_time()
    client = mqtt_setup()
    main()
except Error as e:
    print(f"Error: {e}")
finally:
    client.disconnect()
    print('Disconnected from MQTT broker')
    # machine.reset()

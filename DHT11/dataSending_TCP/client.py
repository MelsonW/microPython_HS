'''
RUN THIS ON YOUR PICOW
'''


import dht
import machine
import network
import socket
import time

# Wi-Fi settings
ssid = 'yourWiFi_ssid'
password = 'password'

# TCP server settings
SERVER_IP = "x.x.x.x"  # your desktop IP
SERVER_PORT = 12345         # port

#dht11 sensor
d = dht.DHT11(machine.Pin(15))
def read_dht11():
    d.measure()
    temp = d.temperature()
    hum = d.humidity()
    return temp, hum

#get time from network
def get_time():
    import ntptime
    ntptime.host = 'time.stdtime.gov.tw'
    ntptime.settime()
    # print(time.localtime())

# connect to Wi-Fi
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    print(wlan.ifconfig())

# create a socket and send data to the TCP server
def send_data(message):
    try:
        addr = socket.getaddrinfo(SERVER_IP, SERVER_PORT)[0][-1]
        sock = socket.socket()  # create a socket
        sock.connect(addr)      # connect to the server
        
        # send the data
        sock.send(message.encode())
        print(f"send message:{message}")

        # 關閉連接
        sock.close()
    except OSError as e:
        print(f"connection or send error:{e}")

#continuous read and publish as json
def main():
    while True:
        temp, hum = read_dht11()
        # temp, hum = random.randint(20, 30), random.randint(40, 60)
        current_time = time.localtime()
        timezone_offset = 8 * 3600
        taiwan_time = time.localtime(time.mktime(current_time) + timezone_offset)
        message = f'{{"CurrentTime":{list(taiwan_time)}, "temperature":{temp}, "humidity":{hum}}}'
        send_data(message)
        time.sleep(5)

# 主程序
try:
    connect()        # connect to Wi-Fi
    get_time()       # get time from network
    main()
except KeyboardInterrupt:
    # machine.reset()
    print("KeyboardInterrupt") 

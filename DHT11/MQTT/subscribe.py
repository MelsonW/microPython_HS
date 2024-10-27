import json
import datetime
import paho.mqtt.client as mqtt
import pymysql

# subscribe topic from mqtt broker

# def on_message(client, userdata, msg):
#     print(f"Received: {msg.topic} -> {msg.payload.decode()}")

#save the received messages into json
messages = []

MYSQL_CONFIG = {
    'host': 'host ip ',                     # Better be external IP
    'user': 'username',  
    'password': 'password',  
    'database': 'BDB_name'  
}

def on_message(client, userdata, msg):
    print(f"Received: {msg.topic} -> {msg.payload.decode()}")
    payload = json.loads(msg.payload.decode())

    current_time_tuple = payload.get("CurrentTime")
    if current_time_tuple:
        current_time_dt = datetime.datetime(*current_time_tuple[:6])
        current_time_str = current_time_dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        # 如果 CurrentTime 不存在，使用當前時間
        current_time_dt = datetime.datetime.now()
        current_time_str = current_time_dt.strftime('%Y-%m-%d %H:%M:%S')

    temp = payload.get("temperature")
    humidity = payload.get("humidity")
    
    message = {
        "current_time": current_time_str,
        "temp": temp,
        "humidity": humidity
    }
   
    messages.append(message)
    with open('messages.json', 'w') as f:
        json.dump(messages, f, indent=4)

def upload_to_mysql(data):
    """
    將資料上傳到 MySQL 資料庫
    :param data: dict, 包含 current_time, temp, humidity 的字典
    """
    try:
        # 連接到 MySQL 資料庫
        connection = pymysql.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()

        # 插入資料到資料庫
        query = """
        INSERT INTO dht11 (time, temp, humidity)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (data['current_time'], data['temp'], data['humidity']))

        # 提交變更
        connection.commit()
    except pymysql.connect.Error as err:
        print(f"MySQL Error: {err}")
    finally:
        cursor.close()
        connection.close()

# Setup MQTT client
client = mqtt.Client()
client.on_message = on_message
# Connect to the broker (your laptop's IP)
client.connect("test.mosquitto.org") # your laptop IP

client.subscribe("pico_w_dht11")


# Start the loop to process received messages
client.loop_forever()

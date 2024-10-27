import socket
import os
import json
import time
import datetime
import pymysql

# setting up the server
HOST =  '0.0.0.0' # represents all available interfaces
PORT = 12345
JSON_FILE = 'sensor_data.json'

MYSQL_CONFIG = {
    'host': 'MySQL_HOST_IP',                # better be external IP
    'user': 'MySQL_username',  
    'password': 'MySQL_password',  
    'database': 'your_database'  
}

# if the file does not exist, create it
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'w') as f:
        json.dump([], f)

#######################FUNCTIONS#######################

def save_data_to_json(data):
    try :
        with open(JSON_FILE, 'r') as f:
            json_data = json.load(f)

        json_data.append(data)

        with open(JSON_FILE, 'w') as f:
            json.dump(json_data, f, indent=4)
        print(f"Data saved to {JSON_FILE}")
    except Exception as e:
        print(f"Error saving data to JSON: {e}")

def convert_datetime_to_str(time_list):
    try:
        current_time_dt = datetime.datetime(*time_list[:6])
        current_time_str = current_time_dt.strftime('%Y-%m-%d %H:%M:%S')
        return current_time_str
    except Exception as e:
        print(f"Error converting time to string: {e}")
        return None

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
        cursor.execute(query, (data['time'], data['temp'], data['humidity']))

        # 提交變更
        connection.commit()
    except pymysql.connect.Error as err:
        print(f"MySQL Error: {err}")
    finally:
        cursor.close()
        connection.close()        

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))

    # listen for incoming connections
    server_socket.listen(5)
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # receive data from client
        data = client_socket.recv(1024).decode()
        print(f"Received: {data}")

        # decode the JSON data
        try:
            parsed_data = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            continue

        # make sure the data is complete
        if 'CurrentTime' in parsed_data and 'temperature' in parsed_data and 'humidity' in parsed_data:
            current_time_str = convert_datetime_to_str(parsed_data['CurrentTime'])
            if current_time_str:
                parsed_data = {
                    'time': current_time_str,
                    'temp': parsed_data['temperature'],
                    'humidity': parsed_data['humidity']
                }
                save_data_to_json(parsed_data)
                upload_to_mysql(parsed_data)
            else:
                print("Data not saved")
        else:
            print("Incomplete data")
    
        
        # client_socket.close()

#######################MAIN#######################

def main():
    start_server()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # main().start_saerver().client_socket.close()
        print("\n Server stopped")

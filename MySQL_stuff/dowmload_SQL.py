import json
import pymysql
import time
from datetime import datetime

MYSQL_CONFIG = {
    'host': 'host ip ',                     # Better be external IP
    'user': 'username',  
    'password': 'password',  
    'database': 'BDB_name'  
}

LOCAL_JSON_FILE = '/path/to/your/file'

current_data = []

def load_local_data(file_path):
    #load data from local JSON file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_local_data(file_path, data):
    #save data to local JSON file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def remove_duplicate_entries(new_data, current_data):
    #remove duplicate entries
    current_times = set(entry['time'] for entry in current_data)
    unique_data = [entry for entry in new_data if entry['time'] not in current_times]
    return unique_data

def convert_datetime_to_str(data):
    #convert datetime objects to string
    for entry in data:
        if isinstance(entry['time'], datetime):
            entry['time'] = entry['time'].strftime('%Y-%m-%d %H:%M:%S')
    return data

def download_from_mysql():
    # dounload data from MySQL and update local JSON file
    global current_data
    try:
        # connect to MySQL server
        connection = pymysql.connect(**MYSQL_CONFIG)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        # search for data
        query = "SELECT time, temp, humidity FROM dht11 ORDER BY time"
        cursor.execute(query)
        new_data = cursor.fetchall()

        # convert datetime objects to string
        new_data = convert_datetime_to_str(new_data)


        # read current data from local JSON file
        current_data = load_local_data(LOCAL_JSON_FILE)
        
        # remove duplicate entries
        unique_data = remove_duplicate_entries(new_data, current_data)
        
        if unique_data:
            # add new data to current data
            current_data.extend(unique_data)
            save_local_data(LOCAL_JSON_FILE, current_data)
            print(f"added {len(unique_data)} data entries")
        else:
            print("no new data to download")
            
    except pymysql.MySQLError as err:
        print(f"MySQL Error: {err}")
    finally:
        cursor.close()
        connection.close()

try:
    while True:
        download_from_mysql()
        time.sleep(5)
except KeyboardInterrupt:
    print("end of download")

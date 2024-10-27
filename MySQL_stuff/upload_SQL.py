'''
This is for uploadin exsist file to MySQL DB
You need to create table first before uploading data
You can learn how to us MySQL here:
https://www.fooish.com/sql/syntax.html
'''

import json
import pymysql

# read json file
with open('/path/to/your/file', 'r', encoding='utf-8') as file:
    data = json.load(file)

# connect to MySQL server
connection = pymysql.connect(
    host = 'host ip ',                     # Better be external IP
    user = 'username',  
    password = 'password',  
    database = 'DB_name'  
)

cursor = connection.cursor()

# insert data
query = """
INSERT INTO dht11 (time, temp, humidity)
VALUES (%s, %s, %s)
"""

for entry in data:
    current_time = entry['current_time']
    temp = entry['temp']
    humidity = entry['humidity']
    cursor.execute(query, (current_time, temp, humidity))

# 提交變更並關閉連線
connection.commit()
cursor.close()
connection.close()

print("upload successfully")

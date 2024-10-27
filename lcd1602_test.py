# import sys

# sys.path.append('//packages/')
# from lcd1602 import lcd1602

from machine import Pin, PWM
from utime import sleep_us, sleep_ms

class lcd1602:
    # constructor
    def __init__(self, rs, e, d4, d5, d6, d7):
        # setup pins
        self.rs = Pin(rs,Pin.OUT)
        self.e = Pin(e,Pin.OUT)
        self.d4 = Pin(d4,Pin.OUT)
        self.d5 = Pin(d5,Pin.OUT)
        self.d6 = Pin(d6,Pin.OUT)
        self.d7 = Pin(d7,Pin.OUT)

        self.rs.value(0)
        self.e.value(0)

        # setup lcd
        self.__send(0b00110011) # set 8bit two times
        self.__send(0b00110010) # set 8bit then 4bit
        self.__send(0b00101000) # set 4bit data length, 2 lines, 5x7 dots
        self.__send(0b110) # increment cursor, no display shift
        self.cursor(True)
        self.clear()

    # execute command
    def __exec_pulse(self):
        self.e.on()
        sleep_us(40)
        self.e.off()
        sleep_us(40)

    # set command
    def __set_data(self, bin4):
        self.d4.value(bin4 & 0b1)
        self.d5.value(bin4 >> 1 & 0b1)
        self.d6.value(bin4 >> 2 & 0b1)
        self.d7.value(bin4 >> 3 & 0b1)

    # send command to display
    def __send(self, byte):
        self.__set_data(byte >> 4)
        self.__exec_pulse()
        self.__set_data(byte & 0b1111)
        self.__exec_pulse()

    # clear screen
    def clear(self):
        self.rs.off()
        self.__send(0b1)
        self.rs.on()
        sleep_ms(2)

    # set cursor home
    def home(self):
        self.rs.off()
        self.__send(0b10)
        self.rs.on()
        sleep_ms(2)

    # set cursor properties
    def cursor(self, blink, underscore = False):
        self.rs.off()
        self.__send(0b1100 | underscore << 1 | blink)
        self.rs.on()

    # write to screen
    def write(self, data):
        for byte in data:
            self.__send(ord(byte))

    # set cursor position
    def position(self, row, column):
        self.rs.off()
        self.__send(0b10000000 | row << 6 | column)
        self.rs.on()

    # write/define custom character
    def character(self, id, data = None):
        if(data != None):
            self.rs.off()
            self.__send(0b1000000 | id << 3)
            self.rs.on()
            for byte in data:
                self.__send(byte)
            self.home()
        else:
            self.__send(id)


######################### Functions #########################
#read 4*4 keypad    
def read_keypad():
    rows = [Pin(8, Pin.IN, Pin.PULL_UP), Pin(7, Pin.IN, Pin.PULL_UP), Pin(6, Pin.IN, Pin.PULL_UP), Pin(5, Pin.IN, Pin.PULL_UP)]
    cols = [Pin(4, Pin.OUT), Pin(3, Pin.OUT), Pin(2, Pin.OUT), Pin(1, Pin.OUT)]
    keys = [
        ['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']
    ]
    


    for col in cols:
        col.value(1)
        for row in rows:
            if row.value() == 1:
                sleep_ms(20)  # debounce delay
                if row.value() == 1:
                    while row.value() == 1:
                        pass
                    return keys[rows.index(row)][cols.index(col)]
        col.value(0)
                    

# def scan_keypad():
#     for row_num, row in enumerate(rows):
#         row.value(0)  # 將當前行設為低電位，激活行
#         for col_num, col in enumerate(cols):
#             if col.value() == 0:  # 如果某列被拉低，表示按鍵被按下
#                 utime.sleep_ms(20)  # 防抖動延遲
#                 if col.value() == 0:  # 再次確認按鍵是否仍被按下
#                     while col.value() == 0:
#                         pass  # 等待按鍵釋放
#                     return keys[row_num][col_num]  # 返回按鍵值
#         row.value(1)  # 將當前行設為高電位，關閉行
#     return None  # 如果沒有按鍵被按下，返回 None
######################### Setup #########################
v0 = PWM(Pin(18))
v0.freq(500)
v0.duty_u16(30000)
# display = lcd1602(rs, e, d4, d5, d6, d7)
display = lcd1602(15, 14, 13, 12, 11, 10)
display.cursor(False)

######################### Main Code #########################
# clear display
# display.clear()
# try:
#     while True:
#         # write to first row
#         display.position(0, 0)
#         display.write("Hello MDFK!")

#         # write to second row
#         display.position(1, 0)
#         display.write("It's ME!")
#         sleep_ms(1000)
# except KeyboardInterrupt:
#     display.clear()
#     display.position(0, 0)
#     display.write("Goodbye shithead!")
#     sleep_ms(1000)
#     display.clear()
#     print("KeyboardInterrupt")

display.clear()
try: 
    i, j = 0, 0
    while i <= 1 and j <= 15:
        key = read_keypad()
        display.position(i, j)
        print('i: %d, j: %d, key: %s' % (i, j, key))
        display.write(str(key))
        if j == 15:
            j = 0
            i += 1
            continue
        j += 1
        sleep_ms(150)
except KeyboardInterrupt:
    display.clear()
    display.position(0, 0)
    display.write("Goodbye shithead!")
    sleep_ms(1000)
    display.clear()
    print("KeyboardInterrupt")


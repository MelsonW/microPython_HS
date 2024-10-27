# micropython library for interfacing
# 1602 displays with rpi pico (using d4-d7)
# written by atrrnt

from machine import Pin
from utime import sleep_us, sleep_ms

# useful sources
# http://web.alfredstate.edu/faculty/weimandn/lcd/lcd_addressing/lcd_addressing_index.html
# https://mil.ufl.edu/3744/docs/lcdmanual/commands.html

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

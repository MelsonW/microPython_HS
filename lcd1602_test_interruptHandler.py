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


######################### SETUP #########################
#read 4*4 keypad    
rows = [Pin(8, Pin.OUT), Pin(7, Pin.OUT), Pin(6, Pin.OUT), Pin(5, Pin.OUT)]
cols = [Pin(4, Pin.IN, Pin.PULL_DOWN), Pin(3, Pin.IN, Pin.PULL_DOWN), Pin(2, Pin.IN, Pin.PULL_DOWN), Pin(1, Pin.IN, Pin.PULL_DOWN)]
# cols = [Pin(4, Pin.IN, Pin.PULL_UP), Pin(3, Pin.IN, Pin.PULL_UP), Pin(2, Pin.IN, Pin.PULL_UP), Pin(1, Pin.IN, Pin.PULL_UP)]
# rows = [Pin(8, Pin.IN, Pin.PULL_UP), Pin(7, Pin.IN, Pin.PULL_UP), Pin(6, Pin.IN, Pin.PULL_UP), Pin(5, Pin.IN, Pin.PULL_UP)]
# cols = [Pin(4, Pin.OUT), Pin(3, Pin.OUT), Pin(2, Pin.OUT), Pin(1, Pin.OUT)]
keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]


#LCD 
v0 = PWM(Pin(18))
v0.freq(500)
v0.duty_u16(30000)
# display = lcd1602(rs, e, d4, d5, d6, d7)
display = lcd1602(15, 14, 13, 12, 11, 10)
display.cursor(False)

# cursor position
i, j = 0, 0


# setup led light 
led = PWM(Pin(20))
led.freq(100)
led.duty_u16(0)


# check if currently in interrrupt handling
global interrupt_handling
interrupt_handling = False 

################FUNCTIONS################

def handle_key_press(key):
    global i, j
    if j == 15:
        j = 0
        i += 1
    print("Key pressed: ", key)
    display.position(i, j)
    display.write(str(key))
    j += 1
    

def scan_keypad(pin):

    # 獲取引腳的數字來識別是哪一列觸發了中斷
    col_num = cols.index(pin)
    # turn off all rows for scanning
    for row in rows:
        row.off()

    for row_num, row in enumerate(rows):
        row.on()
        sleep_ms(40) # debounce delay
        if cols[col_num].value() == 1:
            key = keys[row_num][col_num]
            # print("row %d, col %d" % (row_num, col_num))
            handle_key_press(key)
            # sleep_ms(40)        
            break   
        row.off()
    
    sleep_ms(50) # set a sleep to avoid multiple key press   
    # reset all rows for col interrupt
    for row in rows:
        row.on()
    

def col_pin_irq_handler(pin):
    # print("col %d triggered" % cols.index(pin))
    scan_keypad(pin)
 

def setup_interrupts():   
    for col in cols:
        col.irq(trigger=Pin.IRQ_RISING, handler=col_pin_irq_handler)
        # col.irq(trigger=Pin.IRQ_FALLING, handler=scan_keypad)

######################### Main Code #########################
display.clear()
for row in rows:
    row.on()

setup_interrupts()

try: 
    print("start")
    while True:
        for dc in range(0, 65536, 4096):
            led.duty_u16(dc)
            sleep_ms(10)
        sleep_ms(100)
        for dc in range(65535, -2, -4096):
            led.duty_u16(dc)
            sleep_ms(10)
        sleep_ms(100)
except KeyboardInterrupt:
    display.clear()
    display.position(0, 0)
    display.write("Goodbye shithead!")
    sleep_ms(1000)
    display.clear()
    print("KeyboardInterrupt")

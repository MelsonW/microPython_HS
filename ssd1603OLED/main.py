from machine import Pin, I2C, ADC
import framebuf, sys, time

# import folder containing ssd1306.py
sys.path.append('/ssd1603OLED/') # add path to ssd1306.py
from ssd1306 import SSD1306_I2C

pix_res_x = 128 # ssd1306 horizontal resolution
pix_res_y = 64  # ssd1306 vertical resolution

######################### SETUP keypad #########################
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

##############I2C setup##################
i2c_dev = I2C(1, scl = Pin(27), sda = Pin(26), freq = 400000)   # I2C for SSD1306
i2c_addr = [hex(ii) for ii in i2c_dev.scan()]                   # get I2C address in hex format

if i2c_addr == []:
    print("No I2C device detected")
    sys.exit()
else:
    print("I2C Address      : {}".format(i2c_addr[0]))  # I2C device address
    print("I2C Configuration: {}".format(i2c_dev))      # print I2C params


##############OLED setup##################
oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev)  # SSD1306 OLED display

# oled.write_cmd(0xc0) # flip display to place 0,0 at lower-left corner
adc_2 = ADC(2) # ADC channel 2 for input


############### Functions ################
def handle_key_press(key):
    global i, j
    if j == 16*8:
        j = 0
        i += 10
    print("Key pressed: ", key)
    oled.text(key, j, i)
    oled.show()
    j += 8

def scan_keypad(pin):

    # 獲取引腳的數字來識別是哪一列觸發了中斷
    col_num = cols.index(pin)
    # turn off all rows for scanning
    for row in rows:
        row.off()

    for row_num, row in enumerate(rows):
        row.on()
        time.sleep_ms(40) # debounce delay
        if cols[col_num].value() == 1:
            key = keys[row_num][col_num]
            # print("row %d, col %d" % (row_num, col_num))
            handle_key_press(key)
            # sleep_ms(40)        
            break   
        row.off()
    
    time.sleep_ms(50) # set a sleep to avoid multiple key press   
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

############## Some initial variable  ##################
# Raspberry Pi logo as 32x32 bytearray
buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

# Load the raspberry pi logo into the framebuffer (the image is 32x32)
fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)

# Clear the oled display in case it has junk on it.
i , j = 0, 0 
oled.fill(0)

for row in rows:
    row.on()
setup_interrupts()
try:
    while True:
    #     # Blit the image from the framebuffer to the oled display
    #     oled.blit(fb, 96, 0)

    #     # Add some text
    #     oled.text("Raspberry Pi",5,5)
    #     oled.text("Pico",5,15)

    #     # Finally update the oled display so the image & text is displayed
    #     oled.show()
        time.sleep_ms(50)
except KeyboardInterrupt:
    oled.fill(0)
    oled.show()
    print("\nExiting program")
    sys.exit()
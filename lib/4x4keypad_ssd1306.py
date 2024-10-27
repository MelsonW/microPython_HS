from machine import Pin
from utime import sleep_ms
class keypad():
    def __init__(self, row_pins, col_pins):
        self.row_pins = row_pins
        self.col_pins = col_pins
        self.rows = [Pin(pin, Pin.IN) for pin in row_pins]
        self.cols = [Pin(pin, Pin.OUT, Pin.PILL_DOWN) for pin in col_pins]
        self.keymap = [
            ['1', '2', '3', 'A'],
            ['4', '5', '6', 'B'],
            ['7', '8', '9', 'C'],
            ['*', '0', '#', 'D']
        ]
    
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
from machine import Pin
import utime

# pin16 -> LED, pin18 -> button 0, pin 19 -> button 1
led = Pin(16, Pin.OUT)
button0 = Pin(18, Pin.IN)
button1 = Pin(19, Pin.IN)
print("Press button 0 or button 1")
print("Press Ctrl+C to exit")
led.value(1) #Default LED is off

def button0_handler():
    print("Button 0 is pressed")
    led.value(0)

def button1_handler():
    print("Button 1 is pressed")
    led.value(1)

button0.irq(trigger = Pin.IRQ_FALLING, handler = button0_handler)
button1.irq(trigger = Pin.IRQ_FALLING, handler = button1_handler)



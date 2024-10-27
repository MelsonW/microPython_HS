from machine import Pin
import utime
# pin18 -> LED, pin19 -> button 0, pin 20 -> button 1
led = Pin(16, Pin.OUT)
button0 = Pin(18, Pin.IN)
button1 = Pin(19, Pin.IN)
print("Press button 0 or button 1")
print("Press Ctrl+C to exit")
led.value(1) #Default LED is off
previousStatus = None

# try:
#     while True:
#         input = button0.value()
#         print("Button 0: %d" % input)
#         if input == 0 and previousStatus == input:
#             print("Button 0 pressed")
#             led.value(0)
#             previousStatus = input
# except KeyboardInterrupt:
#     print("KeyboardInterrupt")
#     led.value(1)


try: 
    while True:
        # print("button0: %d, button1: %d" % (button0.value(), button1.value()))
        if button0.value() == 0 :
            led.value(0)
            print("Button 0 pressed")
        elif button1.value() == 0:
            led.value(1)
            print("Button 1 pressed")
except KeyboardInterrupt:
    print("KeyboardInterrupt")
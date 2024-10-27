from machine import Pin, PWM
import utime

led = PWM(Pin(20))
led.freq(100)
led.duty_u16(0)

try:
    while True:
        for dc in range(0, 65536, 4096):
            led.duty_u16(dc)
            utime.sleep(0.1)
        utime.sleep(2)
        for dc in range(65535, -2, -4096):
            led.duty_u16(dc)
            utime.sleep(0.1)
        utime.sleep(2)
except KeyboardInterrupt:
    print("KeyboardInterrupt")
    led.deinit()
    led = Pin(16, Pin.OUT)
    led.value(1)
    print("LED off")
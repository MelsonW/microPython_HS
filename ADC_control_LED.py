from machine import Pin, ADC, PWM
import utime

photoresistor = ADC(Pin(26))
led = PWM(Pin(16))
led.freq(100)
led.duty_u16(0)

def readADC(pin):
    vout = photoresistor.read_u16()
    vout = round(vout * 3.3 / 65535, 2)
    r1 = 330*(3.3-vout)/vout

    return (vout, r1)

try:
    while True:
        vout = readADC(photoresistor)[0]
        r1 = readADC(photoresistor)[1]
        print("Voltage: %f V" % vout)
        print("Resistance: %f ohm" % r1)
        led.duty_u16(1 - photoresistor.read_u16())

        utime.sleep(0.5)
except KeyboardInterrupt:
    print("KeyboardInterrupt")
    print("Exiting program")
  

#Weather Station v1.0p test code

from machine import Pin, I2C
from pyb import CAN, ADC, SPI
import utime


print("starting Weather Station v1.0p test code")
print("v1.0")
print("initializing")
can = CAN(1, CAN.LOOPBACK)
can.setfilter(0, CAN.LIST16, 0, (123, 124, 125, 126))


i2c = I2C(2, freq=100000)

spi = SPI(1, SPI.MASTER, baudrate=600000, polarity=1, phase=0, crc=None)


#initialize temp sensor
print("initializing AHT10 temp sensor")
utime.sleep_ms(200)
i2c.writeto(0x38, b'\xA8')
i2c.writeto(0x38, b'\x00')
i2c.writeto(0x38, b'\x00')


#Setup Pins
hbt_led = Pin("D13", Pin.OUT)
func_butt = Pin("D5", Pin.IN, Pin.PULL_UP)
can_wakeup = Pin("D6", Pin.OUT)
can_wakeup.value(0) 

barometer_cs = Pin("E6", Pin.OUT)
barometer_cs.value(1)



A_BUTTON = Pin("E11", Pin.IN, Pin.PULL_UP)  
B_BUTTON = Pin("E10", Pin.IN, Pin.PULL_UP) 
LIGHT_SENSOR = ADC("A0")

    
#Setup hbt timer
hbt_state = 0
hbt_interval = 500
start = utime.ticks_ms()
next_hbt = utime.ticks_add(start, hbt_interval)
hbt_led.value(hbt_state)


print("starting")


def chk_hbt():
    global next_hbt
    global hbt_state
    now = utime.ticks_ms()
    if utime.ticks_diff(next_hbt, now) <= 0:
        if hbt_state == 1:
            hbt_state = 0
            hbt_led.value(hbt_state)
            #print("hbt")
        else:
            hbt_state = 1
            hbt_led.value(hbt_state)  
        
        next_hbt = utime.ticks_add(next_hbt, hbt_interval)

def chk_buttons():
    global next_button_chk
    now = utime_ms()
    if utime.ticks_diff(next_button_chk, now) <= 0:
        pass
        

def send():
    can.send('message!', 123)   # send a message with id 123
    
def get():
    mess = can.recv(0)
    print(mess)
        

def read_temp_and_humidity():
    i2c.writeto(0x38, b'\xAC')
    i2c.writeto(0x38, b'\x33')
    i2c.writeto(0x38, b'\x00')
    utime.sleep_ms(75)
    print(i2c.readfrom(0x38, 6))

def spi_read(address, num_read):
    buf = bytearray(num_read)
    barometer_cs.value(0)
    spi.send(address)
    spi.recv(buf)
    barometer_cs.value(0)
    print(buf)
    
def get_p():
    spi_read(0xF7, 1)

    
while True:
    chk_hbt()
    if not (func_butt.value()):
        print("function button")
        send()
        utime.sleep_ms(200)
    
    if not (A_BUTTON.value()):
        print("A button")
        print("scanning")
        print(i2c.scan())
        print("light reading:", LIGHT_SENSOR.read())
        utime.sleep_ms(200)
    if not (B_BUTTON.value()):
        print("B button read temp and humidity")
        read_temp_and_humidity()
        utime.sleep_ms(200)






        
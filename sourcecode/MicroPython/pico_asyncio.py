'''
    demo code for Raspberry Pi Pico Breakout Board
    (c)2021 Effevee
    more details on https://github.com/effevee/RPi_Pico_Breakout_Board
    
'''

# modules
from machine import Pin, I2C
import ssd1306
import math
import uasyncio as asyncio

# constants
GREEN = 17
YELLOW = 21
RED = 27
SCL_GPIO = 7
SDA_GPIO = 6
OLED_WIDTH = 128
OLED_HEIGHT = 64
OLED_ADDR = 0x3C


# coroutine for flashing LED
async def flash_led(pin, interval):
    
    # initialise led
    led = Pin(pin, Pin.OUT, value=0)
    
    # blink loop
    while True:
        led.toggle()
        await asyncio.sleep_ms(interval)


# coroutine for calculating prime numbers and displaying them on an OLED display
async def show_prime(maximum):

    # initialise oled
    i2c = I2C(1, sda=Pin(SDA_GPIO), scl=Pin(SCL_GPIO), freq=400000)
    oled = ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr = OLED_ADDR)
    
    # show title on OLED
    oled.fill(0)
    oled.text('Prime numbers', 0, 0)
    
    # primes loop
    for number in range(2,maximum):

        # clear check section of OLED
        oled.fill_rect(0, 20, 128, 10, 0)
        
        # show number being checked
        oled.text('Check %s'%(str(number)), 0, 20)
        oled.show()
        
        # check number is prime ?
        is_prime = True
        for divisor in range(2, math.floor(math.sqrt(number))):
            
            # if number can be divided by divisor, break out of the loop
            if (number % divisor) == 0:
                is_prime = False
                break
            
            # wait for other tasks
            await asyncio.sleep_ms(5)
        
        # show prime on oled
        if is_prime :
            
            # clear found section of OLED
            oled.fill_rect(0, 40, 128, 10, 0)
            
            # show found prime
            oled.text('Found %s'%(str(number)), 0, 40)
            oled.show()
            

# main program
try:
    
    # initialise event loop scheduler
    loop = asyncio.get_event_loop()
    
    # add tasks to event loop queue
    loop.create_task(flash_led(RED, 300))
    loop.create_task(flash_led(YELLOW, 500))
    loop.create_task(flash_led(GREEN, 750))
    loop.create_task(show_prime(100000))
    
    # run tasks
    loop.run_forever()

except Exception as e:
    print('Problem with asyncio - %s'%e)

finally:

    # close event loop scheduler
    loop.close()
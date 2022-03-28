from microbit import *
import radio

radio.on()
radio.config(channel=19)        # Choose your own channel number
radio.config(power=7)   
def fallingBall():
    wait_time = 20e3
    for i in range(5):
        led.toggle(i,2)
        control.wait_micros(wait_time)
        led.toggle(i,2)

display.scroll("hi")
print("error")
fallingBall()
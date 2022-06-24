from microbit import *
import radio


radio.on()
radio.config(channel=19)        # Choose your own channel number
radio.config(power=7)
def fallingBall():
    wait_time = int(20e3)
    for i in range(5):
        display.set_pixel(i,2,9)
        #wait((wait_time,wait_time))    

display.scroll("hi")
#print("error")
fallingBall()

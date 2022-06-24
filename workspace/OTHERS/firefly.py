from microbit import *
import radio
import random
# Create the "flash" animation frames. Can you work out how it's done?
flash = [Image().invert()*(i/9) for i in range(9, -1, -1)]
# The radio won't work unless it's switched on.
radio.on()
radio.config(
    length=64, #maximum message length in bytes up to 251
    queue=10, # max number of messages that can be left in que excess messages are dropped
    channel=20, #integer between 0 and 83 (inclusive)
    power=6, # transmission power max 7
    address=0x75626974, # default used to filter messges 
    group=0, # used with the address when filtering messages 0-255 
    #(which means we might be able to host up to 255 microbits in parallel)
    data_rate=radio.RATE_2MBIT # transfer rate RATE_1MBIT/RATE_2MBIT
    )
while True:
    # Button A sends a "flash" message.
    if button_a.was_pressed():
        radio.send('flash') # a-ha
    # Read any incoming messages.
    incoming = radio.receive()
    if incoming == 'flash':
    # If there's an incoming "flash" message display
    # the firefly flash animation after a random short
    # pause.
        sleep(random.randint(50, 350))
        display.show(flash, delay=100, wait=False)
    #    Randomly re-broadcast the flash message after a
    # slight delay.
    if random.randint(0, 9) == 0:
        sleep(500)
        radio.send('flash') # a-ha
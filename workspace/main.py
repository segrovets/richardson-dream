from microbit import *
import radio
import random

"""
Developed in VSCODE with micro:bit Pyhton extension 
(author: MAKintact)
Code author: segrovets
date: 18/6/2022
notes: for first time user >
commands to microbit are made through ctrl+shift+p menu
for initialisation run 
microbit-python: flash micropython environment to microbit
to then load scipt onto device run
microbit-python: flash sketch on microbit

if multiple devices plugged in its okay, just only last connected devices is used.
"""

me = {
    "num_other_microbits":0,
    "leader_number":0,
    "self_number":0
    }

on_network = [0 for i in range(84)]

current_channel = 8 # dont use channel = 0 for some reason its not v1/v2 scross compatible
display.clear()

# turn on radio
radio.on()
radio.config(
    length=64, #maximum message length in bytes up to 251
    queue=10, # max number of messages that can be left in que excess messages are dropped
    channel=current_channel, #integer between 0 and 83 (inclusive)
    power=6, # transmission power max 7
    address=0x75626974, # default used to filter messges 
    group=0, # used with the address when filtering messages 0-255 
    #(which means we might be able to host up to 255 microbits in parallel)
    data_rate=radio.RATE_2MBIT # transfer rate RATE_1MBIT/RATE_2MBIT
    )

cpt = 0
# set data rate to max and transmission power to max
while True:
    # test the script was correctly loaded, brightness is set 0-9
    #display.set_pixel(2,2,9)
    #display.scroll()
    if button_a.was_pressed():
        radio.send(str(cpt))
        display.scroll(str(cpt))
        cpt = cpt + 1

    
#    details = radio.receive_full()
#    if details: # we write like this in case message que is empty
#        message, RSSI, timestamp = details
#        display.scroll(message)

    message = radio.receive()
    if message:
        display.scroll(message)
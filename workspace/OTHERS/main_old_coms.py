from microbit import *
import radio
import random

import microbit
"""
class microstats():
    def __init__(self):
        self.leader_number= 0
        self.no_other_microbits=0
        self.self_number=0
CLASSES are bugged!
https://forum.makecode.com/t/type-annotation-cannot-appear-on-a-constructor-declaration/4035
"""

me = {"leader_number":0,
        "no_other_microbits":0,
        "self_number":0}


list_devices = [i for i in range(1,84)]
on_network = [0 for i in range(1,84)]

current_group = 1
#print("error")
radio.config(channel=19)

def fallingBall():
    wait_time = 20e3
    for i in range(5):
        display.set_pixel(i,2,9)
        sleep(wait_time)
        display.set_pixel(i,2,9)

def on_button_pressed_a():
    ## only press button a on leader microbit
    if me["self_number"] == me["leader_number"]:
        radio.send(me["self_number"])
    else:
        display.show("!")
        # can do something special

def on_button_pressed_b():
    #fallingBall()
    #control.wait_micros(wait_time*6)
    if me["self_number"] == me["leader_number"]:
        display.show("on net")
        for i in on_network:
            if i != 0:
                display.show("#"+str(i))
    else:
        display.show("i'm"+str(me["self_number"]))

def on_received_number(received):
    received = int(received)
    ## responds to button a press
    ## tells other microbits they are not leader
    ## others then send
    def numberSelf():
        display.show("rec."+str(received))
        me["self_number"] = random.randint(1,83)
        display.show("sen."+str(me["self_number"]))
        sleep(me["self_number"]*1e2)
        radio.send(str(me["self_number"]))
    
    if received == me["leader_number"] and me["self_number"] == me["leader_number"]:
        #message from leader
        numberSelf()  

    elif received == me["self_number"]:
        radio.set_group(me["self_number"]) 

    elif me["self_number"] == me["leader_number"] and received > me["leader_number"]:
        if received not in on_network:
            me["#_other_microbits"] = me["#_other_microbits"] + 1
            display.show("# m:b="+str(me["#_other_microbits"]))
            on_network[received-1]=received
            #send confirmation, you are unique
            radio.send(str(received))
        else:
            radio.config(channel=int(received))
            radio.send(101)
            radio.config(channel=0)

    elif received == 101:
        numberSelf()
    else:
        sleep(1)

def on_recieved(incoming):
    


#radio.on_received_number(on_received_number)]

while True:
    incoming = radio.recieve()
    on_received_number(incoming)
    if button_a.is_pressed():
        on_button_pressed_a()
    elif button_b.is_pressed():
        on_button_pressed_b()
    sleep(100)

#input.on_button_pressed(button_a, on_button_pressed_a)

#input.on_button_pressed(button_b, on_button_pressed_b)
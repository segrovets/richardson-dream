from microbit import *

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


current_group = 1
radio.set_group(current_group)

def fallingBall():
    wait_time = 20e3
    for i in range(5):
        led.toggle(i,2)
        control.wait_micros(wait_time)
        led.toggle(i,2)

def on_button_pressed_a():
    ## only press button a on leader microbit
    radio.send_number(me["self_number"])

def on_button_pressed_b():
    #fallingBall()
    #control.wait_micros(wait_time*6)
    basic.show_number(me["self_number"])

def on_received_number(received):
    ## responds to button a press
    ## tells other microbits they are not leader
    ## others then send
    if received == me["leader_number"]:
        #message from leader
        basic.show_string("rec."+str(received))
        me["self_number"] = randint(1,83)
        basic.show_string("sen."+str(me["self_number"]))
        radio.send_number(me["self_number"])
        radio.set_group(me["self_number"])

    elif me["self_number"] == me["leader_number"] and received > me["leader_number"]:
        me["no_other_microbits"] = me["no_other_microbits"] + 1
        basic.show_string(str(me["no_other_microbits"]))
    else:
        basic.show_string("else"+str(received))
        basic.show_string("self"+str(me["self_number"]))


def on_received_string(received):
    # here we can recieve a data packet and
    # decompress it into components
    # we have all letters and numbers,
    # for example certain characters can be used
    # to seperate information in the packet.
    return 0



radio.on_received_number(on_received_number)

input.on_button_pressed(Button.A, on_button_pressed_a)

input.on_button_pressed(Button.B, on_button_pressed_b)
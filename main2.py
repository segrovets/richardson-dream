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


list_devices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83]
on_network = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

current_group = 1
print("error")
radio.set_group(current_group)

def fallingBall():
    wait_time = 20e3
    for i in range(5):
        led.toggle(i,2)
        control.wait_micros(wait_time)
        led.toggle(i,2)

def on_button_pressed_a():
    ## only press button a on leader microbit
    if me["self_number"] == me["leader_number"]:
        radio.send_number(me["self_number"])
    else:
        basic.show_string("!")
        # can do something special

def on_button_pressed_b():
    #fallingBall()
    #control.wait_micros(wait_time*6)
    if me["self_number"] == me["leader_number"]:
        basic.show_string("on net")
        for i in on_network:
            if i != 0:
                basic.show_string("#"+str(i))
    else:
        basic.show_string("i'm"+str(me["self_number"]))

def on_received_number(received):
    ## responds to button a press
    ## tells other microbits they are not leader
    ## others then send
    def numberSelf():
        basic.show_string("rec."+str(received))
        me["self_number"] = randint(1,83)
        basic.show_string("sen."+str(me["self_number"]))
        control.wait_micros(me["self_number"]*1e2)
        radio.send_number(me["self_number"])
    
    if received == me["leader_number"] and me["self_number"] == me["leader_number"]:
        #message from leader
        numberSelf()  

    elif received == me["self_number"]:
        radio.set_group(me["self_number"]) 

    elif me["self_number"] == me["leader_number"] and received > me["leader_number"]:
        if received not in on_network:
            me["no_other_microbits"] = me["no_other_microbits"] + 1
            basic.show_string("# m:b="+str(me["no_other_microbits"]))
            on_network[received-1]=received
            #send confirmation, you are unique
            radio.send_number(received)
        else:
            radio.set_group(received)
            radio.send_number(101)
            radio.set_group(0)

    elif received == 101:
        numberSelf()
    else:
        control.wait_micros(1)


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
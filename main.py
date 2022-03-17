from microbit import *

leader_number = 0
other_microbits = 0
self_number = 0

wait_time = 20e3
current_group = 1
radio.set_group(current_group)

def fallingBall():
    for i in range(5):
        led.toggle(i,2)
        control.wait_micros(wait_time)
        led.toggle(i,2)

def on_button_pressed_a():
    radio.send_number(leader_number)

def on_button_pressed_b():
    fallingBall()
    control.wait_micros(wait_time*6)
    radio.send_number(current_group)

def on_received_number(received):
    if received == 0:
        #message from leader
        self_number = 1
        radio.send_number(1)

    #if received == 1:


def on_received_string(received):
    # here we can recieve a data packet and 
    # decompress it into components 
    # we have all letters and numbers, 
    # for example certain characters can be used 
    # to seperate information in the packet.
    return 0



radio.on_received_number(on_received_number)

input.on_button_pressed(Button.A, on_button_pressed_a)


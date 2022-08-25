from microbit import *
import radio
import random


me = {
    "num_microbits":1,
    "leader_number":0,
    "self_number":0
    }

radio.on()
current_channel = 0
radio.config(
    length=240, #maximum message length in bytes up to 240
    queue=10, # max number of messages that can be left in que excess messages are dropped
    channel=current_channel, #integer between 0 and 83 (inclusive)
    power=6, # transmission power max 7
    address=0x75626974, # default used to filter messges 
    group=5, # used with the address when filtering messages 0-255 
    data_rate=radio.RATE_1MBIT # transfer rate RATE_1MBIT/RATE_2MBIT NOTE:: only use RATE_1MBIT, RATE_2MBIT is bugged.
    )
    #(which means we might be able to host up to 255 microbits in parallel)

display.clear()

def run_neighbour_test():
    radio.send("nt_"+str(me["self_number"]))

def update_network_list(received):
    on_network = [0]
    for ch in range(1,84): # go through each channel and verify m:b exists on it
        radio.config(channel=ch)
        radio.send("verif")
        sleep(100)
        if (str(received)[0:2]=="v_"): # if we recieve message back
            mb_no = int(str(received)[2:])
            on_network.append(mb_no) # add it to list
  
    radio.config(channel=me["self_number"])
    return on_network

def parallel_task():
    return random.randint()

def parallel_tasker(loops_per_mb):
    _outcomes = []
    for loop in range(loops_per_mb):
        outcome = parallel_task()
        _outcomes.append(outcome)
    return _outcomes

def string_to_list(string):
    #string = string[4:] # remove leading type signifier
    return [element.strip(",").strip("[").strip("]") for element in string.split()]

initialized = False
leader_chosen = False

while True:
    try:
        received = radio.receive()

        ## depending on recived message we perform different functions
        ### Initialization performed by button a press on designated "leader" m:b
        if not initialized:
            
            if ((received == str(me["leader_number"])) and (me["self_number"]==me["leader_number"])):
                """
                (1)
                If leader m:b button a is pressed > All m:b recieve message = 0 > execute below
                All m:b on default channel set themselves to 1 
                All m:b send their new number (1) to default channel
                """
                me["self_number"] = 1
                radio.send("init_"+str(me["self_number"]))
                radio.config(channel=me["self_number"])
                run_neighbour_test()
                sleep(200)

            elif ((str(received) == "init_1") and (me["self_number"]==me["leader_number"])):

                me["num_microbits"] = me["num_microbits"] + 1
                display.show("nmb:"+str(me["num_microbits"]))
                sleep(200)
                display.clear()

            elif ((str(received)[0:3]=="nt_") and (me["self_number"]!=me["leader_number"])):
                # (3) If received then other m:b on your channel and you should switch
                me["self_number"] = me["self_number"] + 1
                radio.config(channel=me["self_number"])
                run_neighbour_test()

            elif ((me["self_number"]!=me["leader_number"])):
                if (str(received)=="verif"):
                    #(4a) checks if only one m:b on each channel
                    radio.send("v_"+str(me["self_number"]))
                    sleep(200)

                elif (str(received)[0:5]=="jump_"):
                    #(4b) instructed to switch channel
                    jump_to = int(str(received)[5:])
                    me["self_number"] = jump_to
                    radio.config(channel=me["self_number"])
                    display.show(jump_to)
                    display.clear()
                    sleep(200)
                    
        if button_a.is_pressed():
            #(1)Begin Init
            
            radio.send(str(me["self_number"]))
            display.show("sent")
            sleep(300)
            leader_chosen = True


    except Exception as e:
        print("Exception!\n{}".format(e))
        display.show("Exception!\n{}".format(e))

    if button_b.is_pressed():
        display.show(me["self_number"])
        sleep(300)
    
    sleep(200)
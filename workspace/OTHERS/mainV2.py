from microbit import *
import radio
import random

"""
Current issue: leader if not recieving the verification response.
"""
me = {
    "num_microbits":1,
    "leader_number":0,
    "self_number":0
    }

initialized = False
leader_chosen = False
n=9
sent_command = False
net_checked = False
on_network = [0]

radio.on()
current_channel = 0
radio.config(
    length=30, #maximum message length in bytes up to 240
    queue=10, # max number of messages that can be left in que excess messages are dropped
    channel=current_channel, #integer between 0 and 83 (inclusive)
    power=6, # transmission power max 7
    address=0x75626974, # default used to filter messges 
    group=5, # used with the address when filtering messages 0-255 
    data_rate=radio.RATE_1MBIT # transfer rate RATE_1MBIT/RATE_2MBIT NOTE:: only use RATE_1MBIT, RATE_2MBIT is bugged.
    )
    #(which means we might be able to host up to 255 microbits in parallel)

display.clear()

def send_to_leader(message):
    radio.config(channel=me["leader_number"])
    radio.send(message)
    radio.config(channel=me["self_number"])

def run_neighbour_test():
    radio.send("nt_"+str(me["self_number"]))

def scan_network():
    for ch in range(1,84): # go through each channel and verify m:b exists on it
        radio.config(channel=ch)
        radio.send("verif")
        display.show(ch) # for debug
        sleep(100)
    radio.config(channel=me["self_number"])

def parallel_task():
    return random.randint(0,9)

def parallel_tasker(loops_per_mb):
    _outcomes = []
    for loop in range(loops_per_mb):
        outcome = parallel_task()
        _outcomes.append(outcome)
    return _outcomes

def string_to_list(string):
    # converts string of a python list back inoto a list
    return [element.strip(",").strip("[").strip("]") for element in string.split()]


while True:
    try:
        received = radio.receive()
        rec_str = str(received)
        ### Initialization performed by button a press on designated "leader" m:b
        if not initialized:
            if rec_str != "None": #4 ddebug
                #display.show("db:"+str(initialized))
                display.show("db:"+rec_str)
            if ((received == str(me["leader_number"])) and (me["self_number"]==me["leader_number"])):
                """
                (1)
                If leader m:b button a is pressed > All m:b recieve message = 0 > execute below
                All m:b on default channel set themselves to 1 
                All m:b send their new number (1) to default channel
                """
                me["self_number"] = 1
                send_to_leader("init_"+str(me["self_number"]))
                run_neighbour_test()
                sleep(200)

            elif ((me["self_number"]==me["leader_number"])):

                if (rec_str == "init_1"):
                    me["num_microbits"] = me["num_microbits"] + 1
                    display.show("nmb:"+str(me["num_microbits"]))
                    sleep(200)
                    display.clear()

                elif (rec_str[0:2]=="v_"): # if we recieve message back
                    mb_no = int(rec_str[2:])
                    print("app : ",mb_no)
                    on_network.append(mb_no) # add it to list  

                elif (leader_chosen and (len(on_network) == me["num_microbits"])):
                    display.show(str(on_network))
                    initialized = True
                    display.show("init")

            elif ((me["self_number"]!=me["leader_number"])):
                if (rec_str[0:3]=="nt_"):
                    # (3) If received then other m:b on your channel and you should switch
                    me["self_number"] = me["self_number"] + 1
                    radio.config(channel=me["self_number"])
                    run_neighbour_test()
                
                elif (str(received)=="verif"):
                    #(4a) checks if only one m:b on each channel
                    send_to_leader("v_"+str(me["self_number"]))
                    initialized = True
                    sleep(200)

                elif (str(received)[0:5]=="jump_"):
                    #(4b) instructed to switch channel
                    jump_to = int(str(received)[5:])
                    me["self_number"] = jump_to
                    radio.config(channel=me["self_number"])
                    display.show(jump_to)
                    display.clear()
                    sleep(200)
        else:
            if rec_str != "None": #4 ddebug
                display.show("db:"+str(rec_str)+str(initialized))
            if (rec_str[:6]=="start_"):
                # perform parallel task (mb 2 not recieving start)
                display.show(rec_str[6:])
                n_loops = int(rec_str[6:])
                outcomes = parallel_tasker(n_loops)
                radio.config(channel=0)
                if me["self_number"] < 10:
                    no_str = "0" + str(me["self_number"])
                else:
                    no_str = str(me["self_number"])
                send_to_leader("mb_"+no_str+"_"+str(outcomes))
                sleep(200)

            elif (me["self_number"]==me["leader_number"]):
          
                if (rec_str[:3]=="mb_"):
                    # if recieved parallel task output
                    sender = int(rec_str[3:5])
                    display.show(sender)
                    message = string_to_list(rec_str[6:])
                    results[sender] = message

        if button_a.is_pressed():
            #(1)Begin Init
            if not leader_chosen:
                radio.send(str(me["self_number"]))
                display.show("sent")
                sleep(300)
                leader_chosen = True

            elif (leader_chosen and not initialized):                
                scan_network()

                sleep(100)
            
            elif initialized and not sent_command:
                results = [0 for n in range(len(on_network))]

                display.clear()
                display.show(str(on_network))
                remainder = n % me["num_microbits"]
                n_per_mb = int(n / me["num_microbits"])
                self_n = n_per_mb + remainder
                for ch in on_network:
                    radio.config(channel=ch)
                    radio.send("start_"+str(n_per_mb))
                sleep(200)
                sent_command = True

            elif sent_command and initialized:
                display.show("r"+str(results))


    except Exception as e:
        print("Exception!\n{}".format(e))
        display.show("Exception!\n{}".format(e))

    if button_b.is_pressed():
        display.show(me["self_number"])
        sleep(3000)
        display.clear()
    
    sleep(200)
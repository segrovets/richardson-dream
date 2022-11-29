from microbit import *
import radio
import random

"""
V3
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
    length=30, #maximum message length in bytes up to 240, large message wil exceed ram
    queue=10, # max number of messages that can be left in que excess messages are dropped
    channel=current_channel, #integer between 0 and 83 (inclusive)
    power=6, # transmission power max 7
    address=0x75626974, # default used to filter messges 
    group=5, # used with the address when filtering messages 0-255 (an alternative to channels?)
    data_rate=radio.RATE_1MBIT # transfer rate RATE_1MBIT/RATE_2MBIT NOTE:: only use RATE_1MBIT, RATE_2MBIT is bugged.
    )
    #(which means we might be able to host up to 255 microbits in parallel)

display.clear()

def send_to_leader(message):
    radio.config(channel=me["leader_number"])
    radio.send(message)
    radio.config(channel=me["self_number"])

def broadcast_all(message):
    for ch in range(84):
        radio.config(channel=ch)
        radio.send(message)
    radio.config(channel=me["self_number"])

def run_neighbour_test():
    radio.send("nt_"+str(me["self_number"]))

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

            elif ((me["self_number"]!=me["leader_number"])):
                if (rec_str[0:3]=="nt_"):
                    # (3) If received then other m:b on your channel and you should switch
                    me["self_number"] = me["self_number"] + 1
                    radio.config(channel=me["self_number"])
                    run_neighbour_test()   
                
                elif (rec_str[:2] == "lc"):
                    leader_chosen = True
                    initialized = True
                    me["num_microbits"] = int(rec_str[2:])

        else:
            if (rec_str[:6]=="start_"):
                display.show("starting")
                sleep(200)
                display.clear()
                n_loops = int(rec_str[6:])
                outcomes = parallel_tasker(n_loops)
                if me["self_number"] < 10:
                    no_str = "0" + str(me["self_number"])
                else:
                    no_str = str(me["self_number"])
                send_to_leader("mb_"+no_str+"_"+str(outcomes))
                display.show("complete")
                sleep(200)
                display.clear()
                sleep(200)

            elif (me["self_number"]==me["leader_number"]):
          
                if (rec_str[:3]=="mb_"):
                    # if recieved parallel task output <<< not working yet
                    sender = int(rec_str[3:5])
                    display.show(sender)
                    message = string_to_list(rec_str[5:])
                    results[sender] = message

        if button_a.is_pressed():
            if not leader_chosen:
                radio.send(str(me["self_number"]))
                display.show("sent")
                sleep(300)
                leader_chosen = True

            elif leader_chosen and not initialized:
                initialized_message = "lc"+str(me["num_microbits"])
                broadcast_all(initialized_message)
                initialized = True
            
            elif ((leader_chosen and initialized)and(me["self_number"]==me["leader_number"]))and(not sent_command):
                display.show("start")
                on_network = [i for i in range(me["num_microbits"])]

                results = [0 for n in range(len(on_network))]

                display.clear()

                display.show(str(on_network))
                remainder = n % me["num_microbits"]
                n_per_mb = int(n / me["num_microbits"])
                self_n = n_per_mb + remainder

                for ch in on_network[1:]:
                    radio.config(channel=ch)
                    radio.send("start_"+str(n_per_mb))
                    display.show("_s_"+str(ch))
                sleep(200)
                display.show("fin")

                results[0] = parallel_tasker(self_n)

                sent_command = True
            
            elif (initialized and sent_command and leader_chosen):
                for index, entry in enumerate(results):
                    for number in entry:
                        display.show("d"+str(index)+"r"+str(number))
                        sleep(300)

    except Exception as e:
        print("Exception!\n{}".format(e))
        display.show("Exception!\n{}".format(e))

    if button_b.is_pressed():
        display.show(me["num_microbits"])
        sleep(3000)
        display.clear()
    
    sleep(200)
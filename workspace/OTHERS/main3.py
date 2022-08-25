from microbit import *
import radio

radio.on()
radio.config(channel=0)

while True:
    try:
        received = radio.receive()
        if received:
            print(received)
    except Exception as e:
        print("Exception!\n{}".format(e))
    if button_a.is_pressed():
        radio.send("hello")
        sleep(300)
    sleep(200)
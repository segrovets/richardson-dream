/** 
class microstats():
    def __init__(self):
        self.leader_number= 0
        self.no_other_microbits=0
        self.self_number=0
CLASSES are bugged!
https://forum.makecode.com/t/type-annotation-cannot-appear-on-a-constructor-declaration/4035

 */
let me = {
    "leader_number" : 0,
    "no_other_microbits" : 0,
    "self_number" : 0,
}

let list_devices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83]
let on_network = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
let current_group = 1
radio.setGroup(current_group)
function fallingBall() {
    let wait_time = 20e3
    for (let i = 0; i < 5; i++) {
        led.toggle(i, 2)
        control.waitMicros(wait_time)
        led.toggle(i, 2)
    }
}

//  can do something special
function on_received_string(received: any): number {
    //  here we can recieve a data packet and
    //  decompress it into components
    //  we have all letters and numbers,
    //  for example certain characters can be used
    //  to seperate information in the packet.
    return 0
}

radio.onReceivedNumber(function on_received_number(received: number) {
    // # responds to button a press
    // # tells other microbits they are not leader
    // # others then send
    function numberSelf() {
        basic.showString("rec." + ("" + received))
        me["self_number"] = randint(1, 83)
        basic.showString("sen." + ("" + me["self_number"]))
        control.waitMicros(me["self_number"] * 1e2)
        radio.sendNumber(me["self_number"])
    }
    
    if (received == me["leader_number"] && me["self_number"] == me["leader_number"]) {
        // message from leader
        numberSelf()
    } else if (received == me["self_number"]) {
        radio.setGroup(me["self_number"])
    } else if (me["self_number"] == me["leader_number"] && received > me["leader_number"]) {
        if (on_network.indexOf(received) < 0) {
            me["no_other_microbits"] = me["no_other_microbits"] + 1
            basic.showString("# m:b=" + ("" + me["no_other_microbits"]))
            on_network[received - 1] = received
            // send confirmation, you are unique
            radio.sendNumber(received)
        } else {
            radio.setGroup(received)
            radio.sendNumber(101)
            radio.setGroup(0)
        }
        
    } else if (received == 101) {
        numberSelf()
    } else {
        control.waitMicros(1)
    }
    
})
input.onButtonPressed(Button.A, function on_button_pressed_a() {
    // # only press button a on leader microbit
    if (me["self_number"] == me["leader_number"]) {
        radio.sendNumber(me["self_number"])
    } else {
        basic.showString("!")
    }
    
})
input.onButtonPressed(Button.B, function on_button_pressed_b() {
    // fallingBall()
    // control.wait_micros(wait_time*6)
    if (me["self_number"] == me["leader_number"]) {
        basic.showString("on net")
        for (let i of on_network) {
            if (i != 0) {
                basic.showString("#" + ("" + i))
            }
            
        }
    } else {
        basic.showString("i'm" + ("" + me["self_number"]))
    }
    
})

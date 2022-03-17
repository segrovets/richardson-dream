class microstats {
    leader_number: number
    no_other_microbits: number
    self_number: number
    constructor(): microstats {
        this.leader_number = 0
        this.no_other_microbits = 0
        this.self_number = 0
    }
    
}

let me = new microstats()
let wait_time = 20e3
let current_group = 1
radio.setGroup(current_group)
function fallingBall() {
    for (let i = 0; i < 5; i++) {
        led.toggle(i, 2)
        control.waitMicros(wait_time)
        led.toggle(i, 2)
    }
}

function on_button_pressed_b() {
    fallingBall()
    control.waitMicros(wait_time * 6)
    radio.sendNumber(current_group)
}

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
    if (received == me.leader_number) {
        // message from leader
        basic.showString("rec." + ("" + received))
        me.self_number = 1
        control.waitMicros(randint(1, 1e4) * 1e3)
        basic.showString("sen.")
        basic.showNumber(me.self_number)
        radio.sendNumber(me.self_number)
    } else if (me.self_number == me.leader_number && received > me.leader_number) {
        me.no_other_microbits = me.no_other_microbits + 1
        basic.showString("" + me.no_other_microbits)
    } else {
        basic.showString("else" + ("" + received))
        basic.showString("self" + ("" + me.self_number))
    }
    
})
input.onButtonPressed(Button.A, function on_button_pressed_a() {
    // # only press button a on leader microbit
    radio.sendNumber(me.self_number)
})

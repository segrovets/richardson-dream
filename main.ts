let leader_number = 0
let other_microbits = 0
let self_number = 0
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

// if received == 1:
function on_received_string(received: any): number {
    //  here we can recieve a data packet and 
    //  decompress it into components 
    //  we have all letters and numbers, 
    //  for example certain characters can be used 
    //  to seperate information in the packet.
    return 0
}

radio.onReceivedNumber(function on_received_number(received: number) {
    let self_number: number;
    if (received == 0) {
        // message from leader
        self_number = 1
        radio.sendNumber(1)
    }
    
})
input.onButtonPressed(Button.A, function on_button_pressed_a() {
    radio.sendNumber(leader_number)
})

import os
import time

'''
GPIO PINS 22 , 23
'''

RMT = 4
RM1 = 17  
RM2 = 27

LMT = 6
LM1 = 22
LM2 = 23

curr_pins = []
prev_direction = 'n'

INPUT_PINS = []
OUTPUT_PINS = [RMT, RM1, RM2, LMT, LM1, LM2]


def write_to_file(content, pin):
    with open(f"/dev/gpio/{pin}", 'w') as f:
        f.write(content)

def power_pin(pin):
    write_to_file('on', pin)

def shut_pin(pin):
    write_to_file('off', pin)

def get_data(pin):
    pass

def clear_curr_pins():
    global curr_pins
    for pin in curr_pins:
        shut_pin(pin)


def setup():
    for pin in OUTPUT_PINS:
        write_to_file("out", pin)

    for pin in INPUT_PINS:
        write_to_file("in", pin)

def validate_input(inp):
    global prev_direction
    r_val = inp
    if (inp == 'w' and prev_direction == 's') or (inp == 's' and prev_direction == 'w'):
        r_val = 'n'
    elif (inp == 'a' and prev_direction == 'd') or (inp == 'd' and prev_direction == 'a'):
        r_val = 'n'
    
    prev_direction = r_val
    
    return r_val

def handle_input(inp):
    match inp:
        case 'w':
            print("HERB is moving forwards")
            go_forwards()
          
        case 'a':
            print("HERB is turning left")
            go_left()
        case 's': 
            print("HERB is going backwards")
            go_backwards()
           
        case 'd':
            print("HERB is turning right")
            go_right()

        case 'n':
            print("HERB stopped!")
           
        case 'q':
            exit()
           
        case _: 
            print("Not a valid input, HERB stopped!")

def go_forwards():
    power_pin(RM1)
    power_pin(RMT)

    power_pin(LM1)
    power_pin(LMT)

    global curr_pins

    curr_pins.append(RM1)
    curr_pins.append(RMT)
    curr_pins.append(LM1)
    curr_pins.append(LMT)

def go_backwards():
    power_pin(RM2)
    power_pin(RMT)

    power_pin(LM2)
    power_pin(LMT)

    global curr_pins

    curr_pins.append(RM2)
    curr_pins.append(RMT)
    curr_pins.append(LM2)
    curr_pins.append(LMT)


def go_left(): 
    power_pin(RM1)
    power_pin(RMT)

    global curr_pins

    curr_pins.append(RM1)
    curr_pins.append(RMT)

def go_right():
    power_pin(LM1)
    power_pin(LMT)

    global curr_pins

    curr_pins.append(LM1)
    curr_pins.append(LMT)

def loop():
    while True:
        ip = input()
        f_ip = validate_input(ip)
        clear_curr_pins()
        handle_input(f_ip)

if __name__ == "__main__":

    setup()

    try:
        loop()

    except KeyboardInterrupt:
        clear_curr_pins()
        exit()
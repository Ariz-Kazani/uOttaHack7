# Right Motor pin numbers (GPIO PIN # on the Raspberry Pi)
RMT = 4
RM1 = 17  
RM2 = 27

# Left Motor pin numbers (GPIO PIN # on the Raspberry Pi)
LMT = 6
LM1 = 22
LM2 = 23

# List of pins that are currently powered
curr_pins = []

# Previous direction of the robot (this is so the opposite direction can be used to stop herb)
prev_direction = 'n'

# List of input pins (if we got to that part)
INPUT_PINS = []

# List of output pins
OUTPUT_PINS = [RMT, RM1, RM2, LMT, LM1, LM2]

# writes data to the pins
def write_to_file(content, pin):
    with open(f"/dev/gpio/{pin}", 'w') as f:
        f.write(content)

# turns the pin on
def power_pin(pin):
    write_to_file('on', pin)

# turns the pin off
def shut_pin(pin):
    write_to_file('off', pin)

# gets the data from the pin
def get_data(pin):
    pass

# clears the current pins that are powered
def clear_curr_pins():
    global curr_pins
    for pin in curr_pins:
        shut_pin(pin)

# initializes the pins to
def setup():
    for pin in OUTPUT_PINS:
        write_to_file("out", pin)

    for pin in INPUT_PINS:
        write_to_file("in", pin)

# validates the input, if the input is the opposite of the previous direction, it will return 'n' to stop the robot
def validate_input(inp):
    global prev_direction
    r_val = inp
    if (inp == 'w' and prev_direction == 's') or (inp == 's' and prev_direction == 'w'):
        r_val = 'n'
    elif (inp == 'a' and prev_direction == 'd') or (inp == 'd' and prev_direction == 'a'):
        r_val = 'n'
    
    prev_direction = r_val
    
    return r_val


# handles the input
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

# moves the robot forwards
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

# moves the robot backwards
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

# moves the robot left
def go_left(): 
    power_pin(RM1)
    power_pin(RMT)

    global curr_pins

    curr_pins.append(RM1)
    curr_pins.append(RMT)

# moves the robot right
def go_right():
    power_pin(LM1)
    power_pin(LMT)

    global curr_pins

    curr_pins.append(LM1)
    curr_pins.append(LMT)

# main loop
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
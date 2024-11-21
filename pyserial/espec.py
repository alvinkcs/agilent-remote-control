import serial
import time
ser = serial.Serial(port='COM4',
baudrate=9600,
timeout=3,
parity=serial.PARITY_NONE,
rtscts=True,
xonxoff=True
)
def run_command():
    print(ser)
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    print('Standard input flow:\n01, ROM?\n01, TEMP?\n01, MODE?\n01, MODE, CONSTANT\n01, TEMP, S23.0')
    while (True):
        val = 0
        # command = '01, MODE, STANDBY'
        command = input('command input (type q to quit):')
        if (command == 'q' or command =='Q'):
            break
        # command += str('\x0a')
        command += str('\r\n')
        val = ser.write(command.encode(encoding='ascii', errors='strict'))
        print('bytes written: ', val)
        in_data = '123'
        in_data = ser.readline()
        print(in_data)
    print('program ended')

def run_test(temp=20):
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    command = "01, MODE, CONSTANT\r\n"
    ser.write(command.encode(encoding='ascii', errors='strict'))
    in_data = ser.readline()
    print(in_data)
    command = "01, TEMP, S{}\r\n".format(temp)
    ser.write(command.encode(encoding='ascii', errors='strict'))
    in_data = ser.readline()
    print(in_data)

def temp_monitor():
    command = "01, TEMP?\r\n"
    ser.write(command.encode(encoding='ascii', errors='strict'))
    in_data = ser.readline()
    return in_data.decode(encoding='ascii', errors='strict')
# ser.close()
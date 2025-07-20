import serial
import argparse
import sys

def init_serial(port):

    #This will need to be changed for your individual device
    s = serial.Serial(port,baudrate=115200,timeout=0.2)
    s.reset_input_buffer()
    s.reset_output_buffer()
    return s

#the main loop of the program, does the work of the terminal emulator
def loop(ser):
    while True:
        i=input('::')
        
        ret_str = command(ser, i)
        
        if not ret_str.endswith('::'):
            print(f"unexpected retun = {from_ser}")
        else:
            print(ret_str[:-2])
            
#runs a series of commands to make sure everything is turned off properly
#when the program is shut down
def cleanup(ser):
    commands = ["rels.off", "chs.off"]
    
    for x in commands:
        command(ser, x)
    
    ser.close()
    
#runs a command
def command(ser, i):
    #ensures command is formated properly
    stripped=i.strip()
    delimited_str=f"{stripped}\r\n"
    
    #encodes and then writes the string. byte count is not utilized
    byte_count=ser.write(delimited_str.encode('utf-8'))
    from_ser = ser.read_until('::')
    
    ret_str=f"{from_ser.decode('utf-8').strip()}"
    
    return ret_str

#starts the main loop, gets out of the loop is control-c (keyboard interrupt) is pressed
if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help = "Name of port (for example: /dev/cu.usbmodem14201). List ports with (python -m serial.tools.list_ports)")
    parser.add_argument("-t", "--temp", help = "Get the temperature and return")
    args = parser.parse_args()

    tempch = args.temp

    port = args.port
    if port == "":
        #example port: /dev/cu.usbmodem14201
        print("You must pass a port variable. Do this using -p.")
        sys.exit()
    my_serial=init_serial(port)
    
    if tempch == "":
        print(f"""Talking to UK1104.
        timeout={my_serial.timeout} seconds
        hit <return> during first connrction with relay
        *use control c to exit*""")
        try:
            loop(my_serial)
        except KeyboardInterrupt:
            print("goodbye")
        except Exception as e:
            print(f"unexpected error: {e}")
        finally:
            cleanup(my_serial)
    else:
        command(my_serial, f"ch{tempch}.on")
        command(my_serial, f"ch{tempch}.setmode(4)")
        print(command(my_serial, f"ch{tempch}.gettemp"))
        
        


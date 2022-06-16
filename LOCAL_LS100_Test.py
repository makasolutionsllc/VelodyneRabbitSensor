import binascii
import socket, time

#Declare static variables for use later
import struct

HOST = "10.245.26.139" # The server's hostname or IP address
PORT = 2112 # The port used by the server
#todo implement a timeout schema

#socket.setdefaulttimeout(3.0)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

DESTINATION_ADDR = HOST
SOURCE_PORT, DESTINATION_PORT = 49829, 2112
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def decode(x):
    '''
    used to return the IEEE specified float result used by SICK on this rangefinder
    :param x:raw input at 32 bit value big endian as transmitted over http
    :return: processed result
    '''
    exp = (x>>30) & 0xff
    mantissa = x&((2**24)-1)
    return 0.1 * mantissa * (2**(exp-15))

def readSick(val):
    '''
    Used to communicate with the sensor, and read various outputs.
    :param val: command string for returning information, where
    : 'info' returns device name, status, information, etc in string.
    : 'distance' returns the float distance to reflector target in mm
    : 'serial' returns the device serial #
    :return:
    '''
    if(val == 'info'):
        outstring = '0202020200000005735249000068' #request device info command
    elif(val == 'distance'):
        outstring = '0202020200000005735249000a62' #request device distance command
    elif(val == 'serial'):
        outstring = '020202020000000573524900036B' #request serial# command
    else:
        outstring = '0202020200000005735249000068' #request device info command

    result = bytearray.fromhex(outstring)
    #print("sending", result)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(result)
        time.sleep(0.1)
        data = s.recv(100)
    if(val == 'info' or val == 'serial'):
        print(f"Received {data!r}")
        #print('index A:',hex(data[11]),'B:',hex(data[12]),'Value:',hex(data[13]),hex(data[14]),hex(data[15]),hex(data[16]))
    elif(val == 'distance'):
        dst = [data[13], data[14], data[15],data[16]]
        data.hex()
        byte_array = bytearray(dst)
        i = data[13:17:1]
        i = binascii.b2a_hex(i)
        f = struct.unpack('>f',binascii.unhexlify(i))
        i = f[0] * 1000
        print(i)



        big = int.from_bytes(byte_array, byteorder='big')
        little = int.from_bytes(byte_array, byteorder='little')
        #for q in range(len(data)):
            #print('Position',q,hex(data[q]))

        #print('data',data, 'index A:',hex(data[11]),'B:',hex(data[12]),'BigEndian =',big, 'Array:', hex(data[13]),hex(data[14]),hex(data[15]),hex(data[16]))
        #print('BigEndian =',big, 'Little',little, hex(data[13]),hex(data[14]),hex(data[15]),hex(data[16]))

#readSick('info')
#readSick('serial')

if __name__ == '__main__':
    print('LS100 test application')
    for x in range(10):
        readSick('distance')
        time.sleep(0.1)

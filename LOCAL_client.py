'''
*   Rabbit interface module
*   Developed by ARC @ 2022
*   for assistance please contact ARC @
*   advancedresearch-consulting.com or advancedresearchconsulting@gmail.com
*   Velodyne project manager for work was Basil Zimmo
'''
import socket, time, struct, cv2, pickle, os
from datetime import datetime

#Declare static variables for use later
HOST = "10.245.26.183"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
#todo implement a timeout schema


def captureandsave():
    s.sendall(b"CAMERA_CAPTURE")
    data = b""  # input
    payload_size = struct.calcsize(">L")
    print("payload_size: {}".format(payload_size))
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += s.recv(4096)

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += s.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    iname = os.path.join(os.path.expanduser('~'), 'Documents',
                         'TARGETIMAGE-' + str(datetime.now().strftime("%H:%M:%S")) + "-test.jpg")

    if not cv2.imwrite(iname, frame):
        raise Exception("Failed to write image to", iname, " - check path / directory exists")
    print("Image saved to", iname)

def runme():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"INFO")
        data = s.recv(1024)
        print(f"Received {data!r}")

        time.sleep(1)

        s.sendall(b"MOVE,120.005")
        data = s.recv(1024)
        print(f"Received {data!r}")

        s.sendall(b"INFO")
        data = s.recv(1024)
        print(f"Received {data!r}")

        captureandsave()


    '''
    s.sendall(b"SHUTDOWN")
    data = s.recv(1024)
    print(f"Received {data!r}")
    s.close()
    '''



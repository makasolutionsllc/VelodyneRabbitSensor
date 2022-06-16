# server example for raspberry pi
import socket

HOST = ''  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            if(data == b"camera"):
                conn.sendall(b"Image returned")
            #conn.sendall(b"Hello, world")

if __name__ == '__main__':
    print('Rabbit communication tester')

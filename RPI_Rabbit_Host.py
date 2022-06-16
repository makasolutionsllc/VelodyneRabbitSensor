'''
Host file activated via crontab on RPI.
File will autoboot each time pi is powered up.

'''


import socket,cv2, pickle, struct, stepperdriver, LevelChanger
import LOCAL_LS100_TEST as LS


HOST = ''  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
ver = "0.0.1"
rabbitinfo = {
    "NAME": "Velodyne Rabbit Control",
    "VERSION": ver,
    "STATUS": "STOPPED",
    "POSITION": 0,
    "MINDIST": None,
    "MAXDIST": None #unit in mm, or 145 meters
    

}

#pull information from config.txt places them into rabbitinfo dict

with open('config.txt', 'r') as e:
    configinfo = e.readlines()
    for x in range(len(configinfo)):
        #can be changed as txt file is updated with more data
        MinDist, MaxDist = configinfo[0], configinfo[1]
    #parses then changes type to int    
    MinDist = int(MinDist[9:])
    MaxDist = int(MaxDist[9:])
    #places variables as Dict Values
    rabbitinfo['MINDIST'] = MinDist
    rabbitinfo["MAXDIST"] = MaxDist



caminfo = {
    "NAME": "Mono IR Camera",
    "VERSION": ver,
    "MODE": "SINGLE",
    "STATUS" : "OFFLINE",
    "ERRORS": "NONE"
}

def start_server():
    '''#add quotes here
    loop runs until command is provided to shut down.
    System boots and waits for an incoming socket connection.\n
    :param data: command sent to the server for execution\n
    "INFO": returns string of information to client about the rabbit.\n
    "MOVE,#": moves rabbit to empirical location, specified in mm, where 0 = the calibrated offset point, closest to operator.\n
    "CAMERA_INFO": returns settings currently selected for the camera.\n
    "CAMERA_INFO": returns settings currently selected for the camera.\n
    "CAMERA_ADJUST,axis,#": where axis = x,y,e and value is the adjustment number, x= width in pixels, y = height in pixels, e = exposure in EV at float 0.1f values.\n
    "CAMERA_CAPTURE" : acquires an image from the camera, image is transferred back to client over http.\n
    "SHUTDOWN": disables further communication from host, shuts down the operating system.\n
    '''#add quotes here

    shutdown = False
    #attempt to set up camera
    cam = cv2.VideoCapture(0)
    cam.set(3,320)
    cam.set(4,240)
    img_counter = 0
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]
    caminfo['STATUS'] = "ONLINE"

    while not shutdown: #only stop if system is told to close connections
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen() #max 5 clients
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")

                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    if(data == b"INFO"):
                        st = "" #empty string
                        lastInfo = rabbitinfo #get recent device info
                        for k in lastInfo: #make a single string for all info
                            st += str(k) + ':' + str(lastInfo[k]) + ','
                        st += 'END'
                        bout = st.encode('utf-8') # convert to byte
                        conn.sendall(bout) # send it

                    elif(b"MOVE" in data):
                        if(rabbitinfo['STATUS'] == "STOPPED"): #only accept a move if not moving and not error
                            inString = data.decode()
                            command = inString.split(',')
                            userDistance = command[1]
                            print('user wants to move to', userDistance)
                            
                            #test range validity against stops
                            buffer =10
                            
                            if(userDistance < (rabbitinfo['MINDIST']+buffer) or userDistance > (rabbitinfo['MAXDIST']-buffer)):
                                if(userDistance < rabbitinfo['MINDIST']):
                                    rabbitinfo['STATUS'] = "MINERROR"
                                    #display led error sequence
                                    LevelChanger.error()
                                    
                                elif(userDistance > rabbitinfo['MAXDIST']):
                                    rabbitinfo['STATUS'] = "MAXERROR"
                                    #display led error sequence
                                    LevelChanger.error()
                                
                                out = "MOVE,"+str(command[1])+",1" #return the move value and throw error code at end
                                conn.sendall(out.encode('utf-8')) # send it
                                print(out)
            
                            else: #move is acceptable
                                rabbitinfo['STATUS'] = "MOVING"
                                conn.sendall(command[1].encode('utf-8')) # send it
                                print(command[1])
                                #userDistance passed safety protocols, sends move command to steppermotor
                                stepperdriver.moveMotor(True, command[1])
                                LevelChanger.moving()
                                time.sleep(1) #provide time for stepper motor to finish moving
                                rabbitinfo['STATUS'] = "STOPPED"
                                siccDist = LS.readSick('distance')
                                siccStr = "Sicc Sensor Distance : ", siccDist
                                conn.sendall(siccStr.encode('utf-8'))
    
                                
                                
                                



                    elif(data == b"CAMERA_INFO"):
                        lastInfo = caminfo #get recent device info
                        for k in lastInfo: #make a single string for all info
                            st += str(k) + ':' + str(lastInfo[k]) + ','
                        st += 'END'
                        bout = st.encode('utf-8') # convert to byte
                        conn.sendall(bout) # send it

                    elif(b"CAMERA_ADJUST" in data): # command,axis,value x y res or e = exposure
                        inString = data.decode()
                        command = inString.split(',')
                        if(command[1] == 'x'):
                            cam.set(3,int(command[2])) #set x resolution
                        if(command[1] == 'y'):
                            cam.set(4,int(command[2])) #set x resolution
                        if(command[1] == 'e'):
                            cam.set(cv2.CAP_PROP_EXPOSURE, int(command[2]))

                        bout = st.encode('utf-8') # convert to byte
                        conn.sendall(bout) # send it

                    elif(data == b"CAMERA_CAPTURE"):
                        ret, frame = cam.read()
                        result, frame = cv2.imencode('.jpg', frame, encode_param)
                        data = pickle.dumps(frame, 0)
                        size = len(data)
                        print("{}: {}".format(img_counter, size))
                        conn.sendall(struct.pack(">L", size) + data)
                        img_counter += 1

                    elif(data == b"SHUTDOWN"):
                        cam.release()
                        conn.sendall("Shutting Down NOW".encode('utf-8')) # send it
                        shutdown = True
                        #TODO - Add shutdown command here


if __name__ == '__main__':
    print('Rabbit Host, use def "start_server" to activate')
    start_server()

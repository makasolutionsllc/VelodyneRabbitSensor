
rabbit_ip = "10.245.26.183"
rabbit_port = 65432

class Target:
    '''controls and communicates with moving target device mounted on rail in test range'''
    def __init__(self,host,port):
        '''
        connects to remote motorized host using host IP and port specified.
        :param host: the ipv4 address of the rabbit device (see bottom of unit)
        :param port: the specified port of the rabbit device (see bottom of unit)
        note for port # this port needs to be accessable/released by internal IT dept.
        '''
        self.connected = False
        try:
            #todo connect to server here
            print("attempting to connect to ",host,":",port)
            print("connection attempt goes here")
            self.connected = True #only once done
        except Exception as e:
            self.connected = False
            print(e)




if __name__ == '__main__':
    print('Rabbit Control Started')
    t = Target(rabbit_ip,rabbit_port)
    print(t.info())

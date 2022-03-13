import socket

def Main():

    host='localhost' #client ip
    port = 4005
    
    server = ('localhost', 4000)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))
    
    message = input("-> ")
    while message !='q':
        s.sendto(message.encode('utf-8'), server)
        reponse, addr = s.recvfrom(1024)
        reponse = reponse.decode('utf-8')
        print("Received from " + str(addr) + " : " + reponse)
        message = input("-> ")
    s.close()

if __name__=='__main__':
    Main()
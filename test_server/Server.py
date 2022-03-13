import socket

def Main():
   
    host = 'localhost' #Server ip
    port = 4000

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    print("Server Started")
    reponse = ""
    while reponse !='q':
        message, addr = s.recvfrom(1024)
        message = message.decode('utf-8')
        print("Message from " + str(addr) + " : " + message)
        reponse = input("-> ")
        print("Sending: " + reponse)
        s.sendto(reponse.encode('utf-8'), addr)
    s.close()

if __name__=='__main__':
    Main()
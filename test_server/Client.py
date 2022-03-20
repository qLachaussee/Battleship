import socket

def Main():

    host = socket.gethostname()
    port = 4005
    
    server = ("DESKTOP-G530RU6", 4000) #l'IPv4 du serveur ou son hostname (host si on travail sur le même PC | "DESKTOP-G530RU6" si on travail avec mon PC perso | "PO-7545" si on travail avec mon PC pro)
    
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
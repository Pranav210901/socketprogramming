import socket


cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 8080

con = False

while True:
    init = input('If you wish to connect to server please type "CONNECT"! ')
    
    if init == "CONNECT":
        try:
            cs.connect((host, port))
            con = True
        except socket.error as e:
            print(str(e))
    
    elif init == "DISCONNECT":
        if con == True:
            cs.send(init.encode("utf-8"))
            wres = cs.recv(1024)
            print(wres.decode("utf-8"))
            cs.close()
            break
        else:
            print("client not connected")
    elif not init:
        pass
    else:
        if con == True:
            cs.send(init.encode("utf-8"))

    res = cs.recv(1024)
    print(res.decode('utf-8'))




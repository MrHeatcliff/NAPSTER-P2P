import socket
from threading import Thread


def new_connection(addr, conn):
    myList = []
    while True:
        data = conn.recv(1024).decode()
        print("Receive from client: " + str(data))
        match data:
            case "ADD LIST":
                if ([addr[0]] + [addr[1]]) not in myList:
                    myList.append([host]+[port])
            case "GET LIST":
                conn.send(str(myList).encode())
        print(myList)
        conn.send("Received".encode())


def server_program(host, port):
    serversocket = socket.socket()
    serversocket.bind((host, port))

    serversocket.listen(10)
    while True: 
        conn, addr = serversocket.accept()
        nconn = Thread(target=new_connection, args=(addr, conn))
        nconn.start()


if __name__ == "__main__":
    host = "192.168.1.33"
    port = 22236
    server_program(host, port)
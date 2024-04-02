import socket
from threading import Thread

myList = []

def new_connection(addr, conn):
    while True:
        data = conn.recv(1024).decode()
        print("Receive from client: " + str(data))
        match data:
            case "ADD LIST":
                conn.send("OK".encode())
                port = int(conn.recv(1024).decode())
                if ([addr[0]] + [port]) not in myList:
                    myList.append([addr[0]]+[port])
            case "GET LIST":
                conn.send(str(myList).encode())
            case _:
                conn.send("Received".encode())
        print(myList)


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
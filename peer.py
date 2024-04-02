import socket
from threading import Thread

myList = []
PEER_SERVER_IP = '192.168.1.33'
PEER_SERVER_PORT = 11234

def new_connection(addr, conn):
    data = conn.recv(1024).decode()
    print(data)
    conn.send("hello".encode())

def peer_server(host, port):
    peerServerSocket = socket.socket()
    peerServerSocket.bind((host, port))

    peerServerSocket.listen(10)
    while True:
        conn, addr = peerServerSocket.accept()
        nconn = Thread(target = new_connection, args = (addr, conn))
        nconn.start()

def peer_client(host, port):
    client_socket = socket.socket()
    client_socket.connect((host, port))
    message = "HELLO"
    client_socket.send(message.encode())
    client_socket.recv(1024).decode()

def separate_string(data):
    data = data.replace("[", "")
    data = data.replace("]", "")
    data = data.replace("\'", "")
    data = data.replace(" ", "")
    splitData = data.split(",")
    for i in range(1, len(splitData), 2):
        splitData[i] = int(splitData[i])
    return splitData

if __name__ == "__main__":
    host = "192.168.1.33"
    port = 22236
    client_socket = socket.socket()
    client_socket.connect((host, port))
    message = "NOPE"
    ser = Thread(target = peer_server, args = ((PEER_SERVER_IP, PEER_SERVER_PORT)))
    ser.start()
    while message.lower().strip() != "bye":
        match message:
            case "ADD LIST":
                client_socket.send(message.encode())
                data = client_socket.recv(1024).decode()
                client_socket.send(str(PEER_SERVER_PORT).encode())
            case "GET LIST":
                client_socket.send(message.encode())
                data = client_socket.recv(1024).decode()
                myList = separate_string(data)
                print(myList)
            case "HELLO":
                for i in range(0, len(myList), 2):
                    cle = Thread(target= peer_client, args= (str(myList[i]), myList[i+1]))
                    cle.start()
            case _:
                client_socket.send(message.encode())
                data = client_socket.recv(1024).decode()
        message = input(" -> ")  # again take input
    client_socket.close()
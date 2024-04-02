import socket
from threading import Thread

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
    my_list = []
    ser = Thread(target = peer_server, args = ((socket.gethostbyname(socket.gethostname()), port)))
    ser.start()
    while message.lower().strip() != "bye":
        match message:
            case "GET LIST":
                client_socket.send(message.encode())
                data = client_socket.recv(1024).decode()
                my_list = separate_string(data)
                print(my_list)
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()

        print('Received from server: ' + data)
        message = input(" -> ")  # again take input
    client_socket.close()
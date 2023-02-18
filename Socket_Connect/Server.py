import socket
import threading

HOST = "127.0.0.1"
PORT = 55555

clients = []  # client socket list


def ClientLoop(conn, addr):
    with conn:
        clients.append(conn)  # add client socket list
        data = conn.recv(1024)  # get first init message
        name = str(data.decode(encoding='UTF-8')).split(" am ")[1]  # pull name from message
        message = f"{name}: {data.decode(encoding='UTF-8')}"
        for client in clients:
            client.sendall(message.encode(encoding='UTF-8'))
        print(f"Connected by {addr} as {name}")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            if data == b"Q":
                conn.sendall(b"Q")
                break
            message = f"{name}: {data.decode(encoding='UTF-8')}"
            print(message)
            for client in clients:
                client.sendall(message.encode(encoding='UTF-8'))
        clients.remove(conn)  # remove client socket list
        print(f"Disconnected by {addr}")
        conn.close()


with socket.socket() as s:
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        threading.Thread(target=ClientLoop, args=(conn, addr)).start()

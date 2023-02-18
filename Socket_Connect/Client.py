import socket
import threading


def Client(name):
    HOST = "127.0.0.1"
    PORT = 55555

    def SendMessage():
        while True:
            message = input()
            if message == "Q":
                s.sendall(b"Q")
                break
            s.sendall(message.encode(encoding="UTF-8"))

    s = socket.socket()
    s.connect((HOST, PORT))
    s.sendall(f"Hello, i am {name}".encode(encoding="UTF-8"))
    print(s.recv(1024).decode(encoding="UTF-8"))
    threading.Thread(target=SendMessage).start()
    while True:
        data = s.recv(1024)
        if not data:
            break
        if data == b"Q":
            break
        print(data.decode(encoding="UTF-8"))
    s.close()

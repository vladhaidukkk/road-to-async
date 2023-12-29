import random
import socket
import sys
import time


def doubler_server(port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", port))
        # start listening to the socket, maximum 5 connections at a time
        s.listen(5)
        while True:
            conn, addr = s.accept()
            handle_connection(conn, addr)


def handle_connection(conn, addr):
    print("Connected by", addr)
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            n = int(data.decode())
            res = f"{n * 2}\n".encode()
            conn.send(res)


def doubler_client(port=8080):
    with socket.create_connection(("127.0.0.1", port)) as s:
        # create a file interface to work with the socket
        f = s.makefile("rw", buffering=1, newline="\n")
        while True:
            n = random.randrange(10)
            f.write(f"{n}\n")
            print(n, f.readline().strip())
            time.sleep(random.random() * 2)


if __name__ == "__main__":
    if sys.argv[1] == "server":
        doubler_server()
    else:
        assert sys.argv[1] == "client", sys.argv[1]
        doubler_client()

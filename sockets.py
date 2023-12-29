import random
import selectors
import socket
import sys
import time


def doubler_server(port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", port))
        # only non-blocking sockets can be added to a selector
        s.setblocking(False)
        s.listen(5)
        sel = selectors.DefaultSelector()
        # add a server socket to the selector and make it read-only (only to accept connections)
        sel.register(s, selectors.EVENT_READ)
        while True:
            # sel.select() blocks until an event occurs (exactly what we need)
            for key, mask in sel.select():
                if key.fileobj is s:
                    conn, addr = s.accept()
                    print("Connected by", addr)
                    # add a connection to the selector to retrieve data from it
                    conn.setblocking(False)
                    sel.register(conn, selectors.EVENT_READ)
                else:
                    conn = key.fileobj
                    data = conn.recv(1024)
                    if not data:
                        conn.close()
                        sel.unregister(conn)
                    n = int(data.decode())
                    res = f"{n * 2}\n".encode()
                    conn.send(res)  # rely on luck, because a socket sending buffer may be full


def doubler_client(port=8080):
    with socket.create_connection(("127.0.0.1", port)) as s:
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

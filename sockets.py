import random
import selectors
import socket
import sys
import time
from enum import Enum, auto


class Op(Enum):
    RECV = auto()
    SEND = auto()


def recv():
    value = yield selectors.EVENT_READ, (Op.RECV, None)
    return value


def send(arg):
    value = yield selectors.EVENT_WRITE, (Op.SEND, arg)
    return value


def run_server(handler, port=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", port))
        s.setblocking(False)
        s.listen(5)
        sel = selectors.DefaultSelector()
        sel.register(s, selectors.EVENT_READ)
        conn_handler_map = {}
        while True:
            for key, mask in sel.select():
                if key.fileobj is s:
                    conn, addr = s.accept()
                    conn.setblocking(False)
                    conn_handler_map[conn] = handler(conn, addr)
                    sel_event, sel_data = conn_handler_map[conn].send(None)
                    sel.register(conn, sel_event, sel_data)
                else:
                    conn = key.fileobj
                    op, arg = key.data
                    sel.unregister(conn)

                    if op is Op.RECV:
                        data = conn.recv(1024)
                    elif op is Op.SEND:
                        conn.send(arg)
                        data = None
                    else:
                        assert False, op

                    try:
                        sel_event, sel_data = conn_handler_map[conn].send(data)
                    except StopIteration:
                        conn.close()
                        del conn_handler_map[conn]
                    else:
                        sel.register(conn, sel_event, sel_data)


def handle_doubler_connection(conn, addr):
    print("Connected by", addr)
    while True:
        data = yield from recv()
        if not data:
            break
        n = int(data.decode())
        res = f"{n * 2}\n".encode()
        yield from send(res)
    print("Disconnected from", addr)


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
        run_server(handle_doubler_connection)
    else:
        assert sys.argv[1] == "client", sys.argv[1]
        doubler_client()

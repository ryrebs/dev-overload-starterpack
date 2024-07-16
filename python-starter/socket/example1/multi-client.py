import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()
messages = [b"msg 1 from client"]  # , b"msg 2 from client"]


def start_connections(host, post, num_conns):
    porti = int(port)
    server_addr = (host, porti)
    ncons = int(num_conns)

    for i in range(0, ncons):
        connid = i + 1
        print(f"Client: starting connection {connid} to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            messages=messages.copy(),
            outb=b"",
        )
        sel.register(sock, events, data=data)


def handle_socket(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
            data.recv_total += len(recv_data)
        if not recv_data or data.recv_total == data.msg_total:
            print(f"Closing connection to {data.connid}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if not data.outb and data.messages:
            data.outb = data.messages.pop(0)
        if data.outb:
            print(f"Sending {data.outb!r} to  connection {data.connid}")
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


host, port, num_conns = sys.argv[1:]
start_connections(host, port, num_conns)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            print(key, mask)
            if key.data is None:
                accept_socket(key.fileobj)
            else:
                handle_socket(key, mask)
except KeyboardInterrupt:
    print("Exiting..")

finally:
    sel.close()

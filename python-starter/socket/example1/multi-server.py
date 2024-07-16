import sys
import socket
import selectors
import types


# Initialization
sel = selectors.DefaultSelector()
host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)  # Set to non blocking
sel.register(lsock, selectors.EVENT_READ, data=None)  # Monitor the socket for events


def accept_socket(sock):
    conn, addr = sock.accept()
    print(f"Server: accepted connection from {addr} with socket {conn}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    print(f"Server: current data {data}")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data)


def handle_socket(key, mask):
    sock = key.fileobj
    data = key.data
    print(f"READ? {mask & selectors.EVENT_READ}")
    print(f"WRITE? {mask & selectors.EVENT_WRITE}")

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
            print(f"Server: received data {data.outb}")
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


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

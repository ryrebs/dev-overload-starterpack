import sys
import socket
import selectors
import types
import traceback

import libserver

sel = selectors.DefaultSelector()
host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)


def accept_socket(sock):
    conn, addr = sock.accept()
    print(f"Server: accepted connection from {addr} with socket {conn}")
    conn.setblocking(False)
    message = libserver.Message(sel, conn, addr)
    sel.register(conn, selectors.EVENT_READ, data=message)


try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            # An empty data means an initial request.
            if key.data is None:
                accept_socket(key.fileobj)
            else:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        f"Main: Error: Exception for {message.addr}:\n"
                        f"{traceback.format_exc()}"
                    )
                    message.close()
except KeyboardInterrupt:
    print("Exiting..")

finally:
    sel.close()

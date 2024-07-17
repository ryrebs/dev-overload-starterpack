import io
import json
import selectors
import struct
import sys


request_search = {
    "morpheus": "Follow the white rabbit. \U0001f430",
    "ring": "In the caves beneath the Misty Mountains. \U0001f48d",
    "\U0001f436": "\U0001f43e Playing ball! \U0001f3d0",
}


class Message:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        self.request = None
        self.response_created = False

    def process_events(self, mask):
        print(f"READ ? {mask & selectors.EVENT_READ}, {mask} {selectors.EVENT_READ}")
        print(f"WRITE ? {mask & selectors.EVENT_WRITE}, {mask} {selectors.EVENT_WRITE}")
        if mask & selectors.EVENT_READ:
            self.read()

        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        try:
            max_bytes_to_read = 4096
            data = self.sock.recv(max_bytes_to_read)
        except BlockingIOError:
            pass
        else:
            # We need to keep track of receive data
            # since there is no guarantee that all of the data
            # is received in a single call.
            if data:
                self._recv_buffer += data
                print(f"Received data: {self._recv_buffer}")
            else:
                raise RuntimeError("Peer closed.")

        # Get the header length
        if self._jsonheader_len is None:
            self.process_protoheader()

        # Get the actual header
        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()

        # Get the body of the message
        if self.jsonheader:
            if self.request is None:
                self.process_request()

    def write(self):
        if self.request:
            if not self.response_created:
                self.create_response()

        self._write()

    def process_protoheader(self):
        """
        Get the header length from the received data.
        """
        # network byte order length
        # (Big-Endian) stores most significant byte is stored at lowest memory address
        # Fix length 2 bytes - common length for network header
        hdrlen = 2

        print(self._recv_buffer[:hdrlen])
        # Checks to make sure enough data is received before getting the header length
        if len(self._recv_buffer) >= hdrlen:
            # Get the header length
            print(f"Struct unpack: {struct.unpack('>H', self._recv_buffer[:hdrlen])}")
            self._jsonheader_len = struct.unpack(">H", self._recv_buffer[:hdrlen])[0]
            print(f"Got json header length {self._jsonheader_len}")

            # Update the receive buffer;remove the header length part
            # Should now contain the header and the data
            self._recv_buffer = self._recv_buffer[hdrlen:]

    def _json_decode(self, json_bytes, encoding):
        tiow = io.TextIOWrapper(io.BytesIO(json_bytes), encoding=encoding)
        obj = json.load(tiow)
        tiow.close()
        return obj

    def process_jsonheader(self):
        """
        Get header from the received data.
        """
        header_len = self._jsonheader_len

        # Checks to make sure enough data is received before getting the header data
        if len(self._recv_buffer) >= header_len:
            # Get the header
            self.jsonheader = self._json_decode(self._recv_buffer[:header_len], "utf-8")

            # Update the receive buffer;remove the header part
            self._recv_buffer = self._recv_buffer[header_len:]

            # Check for required headers
            for req_hdr in (
                "byteorder",
                "content-length",
                "content-type",
                "content-encoding",
            ):
                if req_hdr not in self.jsonheader:
                    raise ValueError(f"Missing required header '{req_hdr}'.")

    def process_request(self):
        """
        Get body from the received data to self.request
        """
        content_len = self.jsonheader["content-length"]

        # Checks to make sure enough data is received before getting the content data
        if not len(self._recv_buffer) >= content_len:
            return

        # Extract data
        data = self._recv_buffer[:content_len]

        # Update the receive buffer;remove the body part
        self._recv_buffer = self._recv_buffer[content_len:]

        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.request = self._json_decode(data, encoding)
            print(f"Received request {self.request!r} from {self.addr}")
        else:
            # Binary or unknown content-type
            self.request = data
            print(
                f"Received {self.jsonheader['content-type']} "
                f"request from {self.addr}"
            )
        # Set selector to listen for write events, we're done reading.
        self._set_selector_events_mask("w")

    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
        # in-memory binary streams or buffered I/O
        json_bytes_ = io.BytesIO(json_bytes)

        # buffered text streams
        b_text_streams = io.TextIOWrapper(json_bytes_)

        obj = json.load(b_text_streams)
        b_text_streams.close()
        return obj

    def _create_response_json_content(self):
        action = self.request.get("action")
        if action == "search":
            query = self.request.get("value")
            answer = request_search.get(query) or f"No match for '{query}'."
            content = {"result": answer}
        else:
            content = {"result": f"Error: invalid action '{action}'."}
        content_encoding = "utf-8"
        response = {
            "content_bytes": self._json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }
        return response

    def _create_response_binary_content(self):
        response = {
            "content_bytes": b"First 10 bytes of request: " + self.request[:10],
            "content_type": "binary/custom-server-binary-type",
            "content_encoding": "binary",
        }
        return response

    def create_response(self):
        if self.jsonheader["content-type"] == "text/json":
            response = self._create_response_json_content()
        else:
            # Binary or unknown content-type
            response = self._create_response_binary_content()
        message = self._create_message(**response)
        self.response_created = True
        self._send_buffer += message

    def _write(self):
        """Send response to client"""
        if self._send_buffer:
            print(f"Sending {self._send_buffer!r} to {self.addr}")
            try:
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                # Update buffer with remaining unsent items
                self._send_buffer = self._send_buffer[sent:]
                if sent and not self._send_buffer:
                    self.close()

    def close(self):
        print(f"Closing connection to {self.addr}")
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(f"Error: selector.unregister() exception for " f"{self.addr}: {e!r}")

        try:
            self.sock.close()
        except OSError as e:
            print(f"Error: socket.close() exception for {self.addr}: {e!r}")
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {mode!r}.")
        self.selector.modify(self.sock, events, data=self)

    def _create_message(self, *, content_bytes, content_type, content_encoding):
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes
        return message

import socket
import time


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((host, port), timeout)

    def __del__(self):
        self.sock.close()

    def _read(self):
        data = b""
        while not data.endswith(b"\n\n"):
            try:
                data += self.sock.recv(1024)
            except socket.error:
                raise ClientError

        decoded_data = data.decode()
        status, payload = decoded_data.split("\n", 1)
        if status != "ok":
            raise ClientError
        payload = payload.strip()
        return payload

    def put(self, key, value, timestamp=int(time.time())):
        self.sock.sendall(f"put {key} {value} {timestamp}\n".encode("utf8"))
        self._read()

    def get(self, key):
        self.sock.sendall(f"get {key}\n".encode("utf8"))
        response = self._read()
        data = {}
        if response == "":
            return data
        for row in response.split("\n"):
            key, value, timestamp = row.split()
            if key not in data:
                data[key] = []
            data[key].append((int(timestamp), float(value)))
        return data


class ClientError(Exception):
    pass

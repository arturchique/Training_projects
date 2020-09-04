import asyncio


ALLOWED_COMMANDS = ("get", "put")
SUCCESS_ANSWER = 'ok\n\n'
WRONG_COMMAND_ANSWER = 'error\nwrong command\n\n'
STORAGE = {}


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = request_parse(data.decode())
        self.transport.write(resp.encode())


def request_parse(data):
    if len(data) > 4 and (data[:3] in ALLOWED_COMMANDS):
        if data[:3] == "get":
            return get_handler(data)
        elif data[:3] == "put":
            return put_handler(data)
        else:
            return WRONG_COMMAND_ANSWER
    else:
        return WRONG_COMMAND_ANSWER


def get_handler(data):
    data = data.split()
    res = "ok\n"
    if len(data) == 2:
        if data[1] == "*":
            for key, value in STORAGE:
                for val in value:
                    res = res + f"{key} {val[0]} {val[1]}\n"
        elif data[1] in STORAGE.keys():
            for val in STORAGE[data[1]]:
                res = res + f"{data[1]} {val[0]} {val[1]}\n"
        return res + "\n"
    else:
        return WRONG_COMMAND_ANSWER


def put_handler(data):
    data = data.split()
    if len(data) == 4:
        if data[1] in STORAGE.keys():
            STORAGE[data[1]].append((int(data[3]), float(data[2])))
        else:
            STORAGE[data[1]] = [(int(data[3]), float(data[2]))]
        return SUCCESS_ANSWER
    else:
        return WRONG_COMMAND_ANSWER


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
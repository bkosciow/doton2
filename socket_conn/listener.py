import json
from threading import Thread
import socket
import regex


class Listener(Thread):
    def __init__(self, address):
        Thread.__init__(self)
        self.address = address
        self.work = True
        self.widgets = {}
        self.connection_error = False
        self.pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')
        self.start_message = regex.compile(r'\d+:{')
        self._connect()

    def _connect(self):
        (addr, port) = self.address.split(":")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # host = socket.gethostname()
        self.socket.connect((addr, int(port)))

    def _recv(self):
        buff = ''
        buff_len = 0
        while True:
            data = self.socket.recv(4096)
            if data:
                data = data.decode('utf8')
                data = data.replace('\n', '')
                elements = self.start_message.findall(data)
                if len(elements):
                    for item in elements:
                        buff_len = int(item[:-2])
                        pos = data.find(item)
                        message = data[pos + len(item) - 1: pos + buff_len + len(item) - 1]
                        if buff_len == len(message):
                            yield message
                        else:
                            buff = message
                else:
                    buff += data
                    if len(buff) == buff_len:
                        yield buff
            else:
                yield None

    def run(self):
        self._initialize_values()
        while self.work:
            try:
                for data in self._recv():
                    # print(">> ", data)
                    if data:
                        try:
                            data = self._decode_data(data)
                            for response in data:
                                key = list(response)[0]
                                self._dispatch_data(key, response[key])
                        except ValueError as e:
                            print("failed to unjonsonify")
                            print(data)
                            print(e)
                    else:
                        self.work = False
                        self.connection_error = True

            except socket.error as e:
                print("socket crash")
                self.work = False
                self.connection_error = True
                print(e)

    def _decode_data(self, data):
        parsed_data = self.pattern.findall(data)
        response = []
        for item in parsed_data:
            response.append(json.loads(item))

        return response

    def _initialize_values(self):
        self.socket.send("getall".encode())

    def stop(self):
        self.work = False

    def add_widget(self, name, widget):
        if name not in self.widgets:
            self.widgets[name] = []

        self.widgets[name].append(widget)

    def _dispatch_data(self, name, data):
        if name in self.widgets:
            for widget in self.widgets[name]:
                widget.update_values(data, name)

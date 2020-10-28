from .storage_pb2_grpc import *
from .storage_pb2 import *
import json
from threading import Thread


class Listener(Thread):
    def __init__(self, address):
        Thread.__init__(self)
        self.address = address
        self.channel = grpc.insecure_channel(address)
        self.stub = ProviderStub(self.channel)
        self.work = True
        self.widgets = {}

    def run(self):
        for response in self.stub.get_changes(EmptyRequest()):
            try:
                response = json.loads(response.data)
                key = list(response)[0]
                self._dispatch_data(key, response[key])
            except ValueError as e:
                response = None

            if response:
                pass

            if not self.work:
                break

    def stop(self):
        self.work = False

    def add_widget(self, name, widget):
        if name not in self.widgets:
            self.widgets[name] = []

        self.widgets[name].append(widget)

    def _dispatch_data(self, name, data):
        print(name, ' <> ', data)
        if name in self.widgets:
            for widget in self.widgets[name]:
                widget.update_values(data)





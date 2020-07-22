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

    def run(self):
        for response in self.stub.get_changes(EmptyRequest()):
            print(response)
            if not self.work:
                break

    def stop(self):
        self.work = False



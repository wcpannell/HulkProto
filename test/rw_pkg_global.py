#!/usr/bin/env

import random
from .__init__ import _PORTS


class PortUser(object):
    def __init__(self, port):
        self.use_port(port)

    def use_port(self, port):
        global _PORTS
        if port not in _PORTS or not _PORTS[port]:
            print(_PORTS)
            self.port = _PORTS[port] = 'PORT OBJECT {}'.format(
                random.randint(0, 10)
            )
            print(_PORTS)
            print(self.port)
        else:
            self.port = _PORTS[port]
            print(_PORTS)
            print(self.port)

    def write(self, message):
        print(message)

    def read(self):
        return str(random.randint(0, 100))

    def query(self, message):
        self.write(message)
        self.read()

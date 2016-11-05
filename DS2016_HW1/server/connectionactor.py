__author__ = 'Taavi'

from socket import *
from common.utilities.actor import *
from time import sleep
import logging
import threading
import common.protocol as P
import Queue


class ConnectionActor(Actor):

    def __init__(self, ip, port):
        Actor.__init__(self)
        self.client_socket = socket(AF_INET, SOCK_STREAM)

        self.ip = ip
        self.port = port
        self.state = self.CONNECTING
        self.receiver = None
        self.name = 'ServerConnectionActor'

        logging.info("Connection started")
        self.start()
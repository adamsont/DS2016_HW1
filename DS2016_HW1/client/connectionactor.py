
__author__ = 'Taavi'

from socket import *
from common.utilities.actor import *
from common.packets.packetparser import *

from time import sleep
import logging
import threading
import common.protocol as P

import Queue


class ConnectionActor(Actor):

    # States
    CONNECTING = 1
    WAITING_PACKET = 2
    IDLE = 3

    def __init__(self, ip, port):
        Actor.__init__(self)
        self.client_socket = socket(AF_INET, SOCK_STREAM)

        self.ip = ip
        self.port = port
        self.state = self.CONNECTING
        self.receiver = None
        self.name = 'ClientConnectionActor'

        logging.info("Connection started")
        self.start()

        #Delegates:
        self.on_update_text = None

    def tick(self):
        #State machine

        if self.state == self.IDLE:
            logging.info("ClientConnection IDLE")
            pass
        elif self.state == self.CONNECTING:
            try:
                logging.info("Trying to connect")
                self.client_socket.connect((self.ip, self.port))

                self.receiver = PacketParser(self.client_socket)
                self.receiver.subscribe(self.on_packet)

                self.state = self.WAITING_PACKET
            except error, exc:
                logging.debug("Socket error")

        elif self.state == self.WAITING_PACKET:
            b = self.client_socket.recv(2)

    def on_packet(self, packet):
        self.message_queue.put(lambda: self.on_packet_handler(packet))

    def on_packet_handler(self, packet):
        packet_type = packet.__class__.__name__
        logging.info("Received: " + packet_type)

        if packet_type == 'UpdateTextPacket':
            option = packet.option
            row = packet.row
            col = packet.column
            text = packet.text

            self.on_update_text(option, row, col, text)

    def terminate(self):
        self.client_socket.shutdown(socket.SHUT_WR)
        self.client_socket.close()

    def sub_on_update_text(self, func):
        self.on_update_text = func




__author__ = 'Taavi'

import logging
from socket import *
from common.utilities.actor import *
from common.packets.packetparser import *
from common.packets.packets import *


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
        self.on_update_text_delegate = None

    def tick(self):
        #State machine

        if self.state == self.IDLE:
            logging.info("ClientConnection IDLE")
            pass
        elif self.state == self.CONNECTING:
            try:
                logging.info("Trying to connect")
                self.client_socket.connect((self.ip, self.port))
                logging.info("Connected to the server")

                self.receiver = PacketParser(self.client_socket)
                self.receiver.sub_on_packet(self.on_packet)
                self.receiver.sub_on_connection_lost(self.on_connection_lost)

                intro = IntroductionPacket("Taavi")
                logging.info("Sending introduction: " + intro.serialize())
                self.client_socket.send(intro.serialize())

                self.state = self.WAITING_PACKET
            except error, exc:
                logging.debug("Socket error: " + str(exc))

        elif self.state == self.WAITING_PACKET:
            pass

    def on_packet(self, packet):
        self.message_queue.put(lambda: self.on_packet_handler(packet))

    def on_connection_lost(self):
        self.client_socket.close()
        self.client_socket = socket(AF_INET, SOCK_STREAM)

        self.state = self.CONNECTING

    def on_packet_handler(self, packet):
        packet_type = packet.__class__.__name__
        logging.info("Received: " + packet_type)

        if packet_type == 'UpdateTextPacket':
            option = packet.option
            row = packet.row
            col = packet.column
            text = packet.text

            self.on_update_text_delegate(option, row, col, text)

    def terminate(self):
        self.client_socket.shutdown(socket.SHUT_WR)
        self.client_socket.close()

    def sub_on_update_text(self, func):
        self.on_update_text_delegate = func



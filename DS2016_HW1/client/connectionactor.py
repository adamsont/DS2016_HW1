
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
        self.c_socket = socket(AF_INET, SOCK_STREAM)

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
                self.c_socket.connect((self.ip, self.port))
                logging.info("Connected to the server")

                self.receiver = PacketParser(self.c_socket)
                self.receiver.on_packet_delegate = self.on_packet
                self.receiver.on_connection_lost_delegate = self.on_connection_lost

                intro = IntroductionPacket("Taavi")
                logging.info("Sending introduction: " + intro.serialize())
                self.c_socket.send(intro.serialize())

                self.state = self.WAITING_PACKET
            except error, exc:
                logging.debug("Socket error: " + str(exc))

        elif self.state == self.WAITING_PACKET:
            pass

    def on_packet(self, packet):
        self.message_queue.put(lambda: self.on_packet_handler(packet))

    def on_connection_lost(self):
        self.c_socket.close()
        self.c_socket = socket(AF_INET, SOCK_STREAM)

        self.state = self.CONNECTING

    def on_packet_handler(self, packet):
        packet_type = packet.__class__.__name__
        logging.info("Received: " + packet_type)

        if packet_type == 'UpdateTextPacket':
            self.on_update_text_delegate(packet)

    def terminate(self):
        self.c_socket.shutdown(socket.SHUT_WR)
        self.c_socket.close()

    def sub_on_update_text(self, func):
        self.on_update_text_delegate = func

    def send_text_update(self, option, row, col, text):
        self.message_queue.put(lambda: self.send_text_update_handler(option, row, col, text))

    def send_text_update_handler(self, option, row, col, text):
        packet = UpdateTextPacket(option, row, col, text)
        logging.info("Sending text update: " + packet.serialize())
        self.c_socket.send(packet.serialize())

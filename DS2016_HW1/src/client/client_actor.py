
__author__ = 'Taavi'

import logging
from socket import *
from common.utilities.actor import *
from common.packets.packetparser import *
from common.packets.packets import *


class ClientActor(Actor):

    # States
    CONNECTING = 1
    DOWNLOADING_DOCUMENT = 2
    WAITING_PACKET = 3
    IDLE = 4

    def __init__(self, ip, port):
        Actor.__init__(self)
        self.c_socket = socket(AF_INET, SOCK_STREAM)

        self.ip = ip
        self.port = port
        self.state = self.CONNECTING
        self.parser = None
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

                self.parser = PacketParser(self.c_socket)
                self.parser.on_packet_delegate = self.on_packet
                self.parser.on_connection_lost_delegate = self.on_connection_lost

                intro = IntroductionPacket("Taavi")
                logging.info("Sending introduction: " + intro.serialize())
                self.c_socket.send(intro.serialize())

                self.state = self.WAITING_PACKET

            except error, exc:
                pass

        elif self.state == self.DOWNLOADING_DOCUMENT:
            pass

        elif self.state == self.WAITING_PACKET:
            pass

    #
    # PUBLIC
    #

    def on_packet(self, packet):
        self.message_queue.put(lambda: self.on_packet_handler(packet))

    def send_text_update(self, option, row, col, text):
        self.message_queue.put(lambda: self.send_text_update_handler(option, row, col, text))

    def on_connection_lost(self):
        self.message_queue.put(lambda: self.on_connection_lost_handler())
        
    #
    # PRIVATE
    #

    def on_connection_lost_handler(self):
        self.c_socket.close()
        self.c_socket = socket(AF_INET, SOCK_STREAM)

        self.parser.stop()
        self.parser = None

        self.state = self.CONNECTING

    def on_packet_handler(self, packet):
        packet_type = packet.__class__.__name__
        logging.info("Received: " + packet_type)

        if packet_type == 'UpdateTextPacket':
            self.on_update_text_delegate(packet)

    def terminate(self):
        self.c_socket.shutdown(socket.SHUT_WR)
        self.c_socket.close()

    def send_text_update_handler(self, option, row, col, text):
        packet = UpdateTextPacket(option, row, col, text)
        logging.info("Sending text update: " + packet.serialize())
        self.c_socket.send(packet.serialize())

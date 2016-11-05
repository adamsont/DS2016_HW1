__author__ = 'Taavi'

from socket import *
from common.packets.packets import *
from common.packets.packetparser import *

from time import sleep
import logging
import threading
import common.protocol as P
import Queue


class Connection:

    #
    # States
    #

    WAITING_INTRODUCTION = 1
    ESTABLISHED = 2

    def __init__(self, c_socket, c_address, c_id="Unknown"):
        self.c_socket = c_socket
        self.c_address = c_address
        self.c_id = c_id

        self.state = self.WAITING_INTRODUCTION
        self.parser = PacketParser(c_socket)
        self.parser.sub_on_packet(self.process_packet)

    def process_packet(self, packet):
        packet_type = packet.__class__.__name__
        logging.info("Received: " + packet_type)

        if packet_type == 'UpdateTextPacket':
            self.process_update_text_packet(packet)

        if packet_type == "IntroductionPacket":
            self.process_introduction_packet(packet)

    def process_update_text_packet(self, packet):
        option = packet.option
        row = packet.row
        col = packet.column
        text = packet.text

    def process_introduction_packet(self, packet):
        if self.state == self.WAITING_INTRODUCTION:
            logging.info("Client at: " + str(self.c_address) + " introduced as: " + packet.c_id)
            self.c_id = packet.c_id
            self.state = self.ESTABLISHED

        else:
            logging.info("Client at: " + str(self.c_address) + " reintroduced as: " + packet.c_id)
            self.c_id = packet.c_id
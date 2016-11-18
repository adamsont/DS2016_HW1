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

    def __init__(self, c_socket, c_address, c_name="Unknown"):
        self.c_socket = c_socket
        self.c_address = c_address
        self.c_name = c_name
        self.c_id = c_address[1]

        self.state = self.WAITING_INTRODUCTION

        self.parser = PacketParser(c_socket)
        self.parser.on_packet_delegate = self.on_packet
        self.parser.on_connection_lost_delegate = self.on_connection_lost

        #Delegates
        self.on_update_text_delegate = None
        self.on_connection_lost_delegate = None

    def on_packet(self, packet):
        packet_type = packet.__class__.__name__
        logging.info("Received: " + packet_type)

        if packet_type == 'UpdateTextPacket':
            self.process_update_text_packet(packet)

        if packet_type == "IntroductionPacket":
            self.process_introduction_packet(packet)

    def on_connection_lost(self):
        self.c_socket.close()
        self.on_connection_lost_delegate(self.c_id)
        
    def process_update_text_packet(self, packet):
        self.on_update_text_delegate(self.c_id, packet)

    def process_introduction_packet(self, packet):
        if self.state == self.WAITING_INTRODUCTION:
            logging.info("Client at: " + str(self.c_address) + " introduced as: " + packet.c_name)
            self.c_name = packet.c_name
            self.state = self.ESTABLISHED

        else:
            logging.info("Client at: " + str(self.c_address) + " reintroduced as: " + packet.c_name)
            self.c_name = packet.c_name

    def send_packet(self, packet):
        logging.info("Sending packet: " + packet.serialize())
        self.c_socket.send(packet.serialize())

    def get_cid(self):
        return self.c_id
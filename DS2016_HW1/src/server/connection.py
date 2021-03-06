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

        self.document_text = "11111\n22222\n33333\n44444\n55555\n66666\n77777\n"
        self.currently_received_document = ''

        self.state = self.WAITING_INTRODUCTION

        self.parser = PacketParser(c_socket)
        self.parser.on_packet_delegate = self.on_packet
        self.parser.on_connection_lost_delegate = self.on_connection_lost

        #Delegates
        self.on_update_text_delegate = None
        self.on_connection_lost_delegate = None
        self.on_document_received_delegate = None
        self.on_document_requested_delegate = None

    def on_packet(self, packet):
        packet_type = packet.__class__.__name__
        logging.info("Received: " + packet_type)

        if packet_type == 'UpdateTextPacket':
            self.process_update_text_packet(packet)

        elif packet_type == "IntroductionPacket":
            self.process_introduction_packet(packet)

        elif packet_type == "DocumentRequestPacket":
            self.process_document_request_packet(packet)

        elif packet_type == "DocumentSendPacket":
            self.process_document_send_packet(packet)

    def on_connection_lost(self):
        self.c_socket.close()
        self.on_connection_lost_delegate(self.c_id)
        
    def process_update_text_packet(self, packet):
        self.on_update_text_delegate(self.c_id, packet)

    def process_introduction_packet(self, packet):
        if self.state == self.WAITING_INTRODUCTION:
            c_name = packet.c_name
            logging.info("Client at: " + str(self.c_address) + " introducing as: " + c_name)
            self.c_name = c_name

        else:
            logging.info("Client at: " + str(self.c_address) + " reintroduced as: " + packet.c_name)
            self.c_name = packet.c_name

    def process_document_request_packet(self, packet):
        self.on_document_requested_delegate(self.c_id, packet.file_name)

    def process_document_send_packet(self, packet):
        total_chunks = packet.total_chunks
        current_chunk = packet.chunk_id

        logging.info("Processing document chunk: " + str(current_chunk) + " of " + str(total_chunks))
        self.currently_received_document += packet.chunk

        if current_chunk == total_chunks:
            logging.info("Successfully downloaded whole document")
            self.on_document_received_delegate(self.c_id, self.currently_received_document)
            self.currently_received_document = ''

    def send_packet(self, packet):
        logging.info("Sending packet: " + packet.serialize())
        self.c_socket.send(packet.serialize())

    def send_document(self, doc_text):
        logging.info("Sending client: " + self.c_name + " document")
        chunk_size = 500
        chunks = [doc_text[i:i+chunk_size] for i in range(0, len(doc_text),chunk_size)]
        total_chunks = len(chunks)
        count = 1

        for chunk in chunks:
            ddp = DocumentSendPacket(count, total_chunks, chunk)
            self.send_packet(ddp)
            count += 1

    def get_cid(self):
        return self.c_id

    def get_cname(self):
        return self.c_name

__author__ = 'Taavi'

import logging
from socket import *
from common.utilities.actor import *
from common.packets.packetparser import *
from common.packets.packets import *


class ClientActor(Actor):

    # States
    CONNECTING = 1
    WAIT_DOWNLOAD_RESPONSE = 2
    DOWNLOADING_DOCUMENT = 3
    WAITING_PACKET = 4
    IDLE = 5

    def __init__(self, ip, port, user_name):
        Actor.__init__(self)
        self.c_socket = socket(AF_INET, SOCK_STREAM)

        self.ip = ip
        self.port = port
        self.user_name = user_name

        self.currently_downloaded_document = ''

        self.state = self.CONNECTING
        self.parser = None
        self.name = 'ClientConnectionActor'

        logging.info("Connection started")
        self.start()

        #Delegates:
        self.on_update_text_delegate = None
        self.on_document_delegate = None

    def tick(self):
        #State machine

        if self.state == self.IDLE:
            pass
        elif self.state == self.CONNECTING:
            try:
                logging.info("Trying to connect")
                self.c_socket.connect((self.ip, self.port))
                logging.info("Connected to the server")

                self.parser = PacketParser(self.c_socket)
                self.parser.on_packet_delegate = self.on_packet
                self.parser.on_connection_lost_delegate = self.on_connection_lost

                intro = IntroductionPacket(self.user_name)
                logging.info("Sending introduction: " + intro.serialize())
                self.send_packet(intro)

                drp = DocumentRequestPacket('correct')
                logging.info("Requesting current document")
                self.send_packet(drp)

                self.state = self.WAIT_DOWNLOAD_RESPONSE

            except error, exc:
                pass
        elif self.state == self.WAIT_DOWNLOAD_RESPONSE:
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

    def send_document(self, text):
        self.message_queue.put(lambda: self.send_document_handler(text))
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
        elif packet_type == "RequestResponsePacket":
            self.process_request_response(packet)
        elif packet_type == "DocumentSendPacket":
            self.process_document_download_packet(packet)

    def terminate(self):
        self.c_socket.shutdown(socket.SHUT_WR)
        self.c_socket.close()

    def send_text_update_handler(self, option, row, col, text):
        packet = UpdateTextPacket(option, row, col, text)
        logging.info("Sending text update: " + packet.serialize())
        self.c_socket.send(packet.serialize())

    def send_packet(self, packet):
        logging.debug("Sent packet: " + packet.serialize())
        self.c_socket.send(packet.serialize())

    def process_request_response(self, packet):
        resp = packet.response
        if self.state == self.WAIT_DOWNLOAD_RESPONSE:
            if resp == 'Y':
                logging.info("Server accepted document request")
                self.state = self.DOWNLOADING_DOCUMENT
            else:
                logging.info("Server declined document request")
                #TODO! let client know that this document is not available
                pass

    def process_document_download_packet(self, packet):
        total_chunks = packet.total_chunks
        current_chunk = packet.chunk_id

        logging.info("Processing download chunk: " + str(current_chunk) + " of " + str(total_chunks))
        self.currently_downloaded_document += packet.chunk

        if current_chunk == total_chunks:
            logging.info("Successfully downloaded whole document")
            self.on_document_delegate(self.currently_downloaded_document)
            self.currently_downloaded_document = ''
            if self.state == self.DOWNLOADING_DOCUMENT:
                self.state = self.IDLE

    def send_document_handler(self, doc_text):
        logging.info("Sending server a document")
        chunk_size = 500
        chunks = [doc_text[i:i+chunk_size] for i in range(0, len(doc_text),chunk_size)]
        total_chunks = len(chunks)
        count = 1

        for chunk in chunks:
            ddp = DocumentSendPacket(count, total_chunks, chunk)
            self.send_packet(ddp)
            count += 1
__author__ = 'Taavi'

import threading
import logging

from packets import *


class PacketParser(threading.Thread):

    WAITING_PACKET_HEADER = 1
    COMBINING_HEADER = 2
    COMBINING_PACKET = 3

    def __init__(self, receive_socket):
        threading.Thread.__init__(self)
        self.subscribers = list()
        self.receive_socket = receive_socket
        self.current_payload_length = 0
        self.current_header = 0
        self.current_payload_buffer = ''
        self.header_buffer = ''
        self.state = self.WAITING_PACKET_HEADER
        self.start()

    def run(self):
        while True:
            data = self.receive_socket.recv(2000)
            #logging.info(data)

            for item in data:
                if self.state == self.WAITING_PACKET_HEADER:
                    if item == P.PACKET_START:
                        self.header_buffer += item
                        self.state = self.COMBINING_HEADER

                elif self.state == self.COMBINING_HEADER:
                    self.header_buffer += item
                    if len(self.header_buffer) == 9:
                        logging.info("Got header, checking")
                        if P.check_header(self.header_buffer):
                            self.current_header = int(self.header_buffer.split(P.HEADER_FIELD_SEPARATOR)[1])
                            self.current_payload_length = int(self.header_buffer.split(P.HEADER_FIELD_SEPARATOR)[2])
                            self.state = self.COMBINING_PACKET
                        else:
                            logging.info("Check failed")
                            self.state = self.WAITING_PACKET_HEADER

                        self.header_buffer = ''

                elif self.state == self.COMBINING_PACKET:
                    self.current_payload_buffer += item

                    if len(self.current_payload_buffer) == self.current_payload_length:
                        logging.info("Got a packet, header: (" + str(self.current_header) + \
                                     ") payload: (" + self.current_payload_buffer + ")")

                        packet = self.try_parse_packet(self.current_header, self.current_payload_buffer)
                        if packet is not None:
                            self.on_packet(packet)

                        self.current_payload_buffer = ''
                        self.state = self.WAITING_PACKET_HEADER

            #data = data[start:]
            #for subscriber in self.subscribers:
            #    subscriber(data)

    def subscribe(self, func):
        self.subscribers.append(func)

    def on_packet(self, packet):
        for subscriber in self.subscribers:
            subscriber(packet)

    def try_parse_packet(self, header, payload):
        packet = None
        count = 0

        while packet is None or count < 1:
            if count == 0:
                packet = UpdateTextPacket.try_parse(header, payload)

            count += 1

        return packet

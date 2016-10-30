__author__ = 'Taavi'

from socket import *
from common.utilities.actor import *
from time import sleep
import logging
import threading
import common.protocol as P
import Queue


class ReceiverThread(threading.Thread):

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

                        self.current_payload_buffer = ''
                        self.state = self.WAITING_PACKET_HEADER

            #data = data[start:]
            #for subscriber in self.subscribers:
            #    subscriber(data)

    def subscribe(self, func):
        self.subscribers.append(func)

class ClientConnection(Actor):

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

    def tick(self):
        #State machine

        if self.state == self.IDLE:
            logging.info("ClientConnection IDLE")
            pass
        elif self.state == self.CONNECTING:
            try:
                logging.info("Trying to connect")
                self.client_socket.connect((self.ip, self.port))

                self.receiver = ReceiverThread(self.client_socket)
                self.receiver.subscribe(self.on_data)

                self.state = self.WAITING_PACKET
            except error, exc:
                logging.debug("Socket error")

        elif self.state == self.WAITING_PACKET:
            b = self.client_socket.recv(2)

    def on_data(self, data):
        self.message_queue.put(lambda: self.on_data_handler(data))

    def on_data_handler(self, data):
        logging.info("Received: " + data)

    def terminate(self):
        self.client_socket.shutdown(socket.SHUT_WR)
        self.client_socket.close()



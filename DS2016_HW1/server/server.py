__author__ = 'Taavi'

from socket import *

import common.protocol as P

import logging

logging.basicConfig(level=logging.DEBUG)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((P.SERVER_HOST, P.SERVER_PORT))
server_socket.listen(1)

while True:
    connection, address = server_socket.accept()
    logging.info("Connected by: " + str(address))

    for i in range(10):
        payload = "Hello :!||||:::!" + str(i)
        packet_type = format(P.DEBUG_MESSAGE, '02d')
        payload_length = format(len(payload), '03d')
        packet = P.PACKET_START + \
                 P.HEADER_FIELD_SEPARATOR + \
                 packet_type + \
                 P.HEADER_FIELD_SEPARATOR + \
                 payload_length + \
                 P.HEADER_FIELD_SEPARATOR + \
                 payload

        logging.info("Sending packet: <" + packet + ">")
        connection.send(packet)

server_socket.shutdown(socket.SHUT_WR)
server_socket.close()


__author__ = 'Taavi'

from socket import *

import common.Protocol as P
import common.packets.Packets as Packets

import logging

logging.basicConfig(level=logging.DEBUG)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((P.SERVER_HOST, P.SERVER_PORT))
server_socket.listen(1)

while True:
    connection, address = server_socket.accept()
    logging.info("Connected by: " + str(address))

    for i in range(10):
        packet = Packets.UpdateTextPacket('A', i, i*10, 'ABCD')
        message = packet.serialize()

        logging.info("Sending packet: <" + message + ">")
        connection.send(message)

server_socket.shutdown(socket.SHUT_WR)
server_socket.close()


__author__ = 'Taavi'

from socket import *

import common.protocol as P
import common.packets.packets as Packets

import logging

logging.basicConfig(level=logging.DEBUG)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((P.SERVER_HOST, P.SERVER_PORT))
server_socket.listen(1)

while True:
    connection, address = server_socket.accept()
    logging.info("Connected by: " + str(address))

    for i in range(10):
        packet = Packets.UpdateTextPacket('A', i, i*10, str(i*100))
        message = packet.serialize()

        logging.info("Sending packet: <" + message + ">")
        connection.send(message)

    packet = Packets.UpdateTextPacket('D', 1, 0, '1234567890')

    connection.send(packet.serialize())
    connection.send(packet.serialize())

server_socket.shutdown(socket.SHUT_WR)
server_socket.close()


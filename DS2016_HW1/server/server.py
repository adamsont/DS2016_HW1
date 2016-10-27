__author__ = 'Taavi'

from socket import *
from common.protocol import *

import logging

logging.basicConfig(level=logging.DEBUG)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)

while True:
    connection, address = server_socket.accept()
    logging.info("Connected by: " + str(address))

server_socket.shutdown(socket.SHUT_WR)
server_socket.close()


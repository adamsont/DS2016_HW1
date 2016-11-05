__author__ = 'Taavi'

from socket import *

import common.protocol as P
from common.packets.packets import *
from connection import *
from collaborationgroup import *

import logging

logging.basicConfig(level=logging.DEBUG)

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((P.SERVER_HOST, P.SERVER_PORT))
server_socket.listen(1)

collaboration_group = CollaborationGroup()

while True:
    conn, addr = server_socket.accept()
    logging.info("New incoming connection from: " + str(addr))
    new_connection = Connection(conn, addr)

    collaboration_group.add_collaborator(new_connection)

server_socket.shutdown(socket.SHUT_WR)
server_socket.close()


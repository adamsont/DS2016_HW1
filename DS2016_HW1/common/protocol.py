__author__ = 'Taavi'


SERVER_HOST = '127.0.0.1'
SERVER_PORT = 47413

PACKET_START = '!'
HEADER_FIELD_SEPARATOR = '|'
PAYLOAD_FIELD_SEPARATOR = ':'

#
# Packet headers
#

#
# Client -> Server
#

INTRODUCTION = 1
REQUEST_DOCUMENT_LIST = 2
REQUEST_DOCUMENT = 3

#
# Server -> Client
#

CONFIRMATION = 11
RESPOND_DOCUMENT_LIST = 12
RESPOND_DOCUMENT = 13
DEBUG_MESSAGE = 99

#
# Server <-> Client
#

UPDATE_TEXT_DELETED = 20
UPDATE_TEXT_ADDED = 21

headers = [INTRODUCTION,
           REQUEST_DOCUMENT_LIST,
           REQUEST_DOCUMENT,
           CONFIRMATION,
           RESPOND_DOCUMENT_LIST,
           UPDATE_TEXT_DELETED,
           UPDATE_TEXT_ADDED,
           DEBUG_MESSAGE]

def check_header(header):
    parts = header.split(HEADER_FIELD_SEPARATOR)
    if len(parts) != 4:
        return False

    if len(parts[1]) != 2:
        return False

    if len(parts[2]) != 3:
        return False

    return True
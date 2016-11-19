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
DOCUMENT_REQUEST = 3

#
# Server -> Client
#

REQUEST_RESPONSE = 11
REQUEST_NOT_OK = 12
RESPOND_DOCUMENT_LIST = 13
DOCUMENT_DOWNLOAD = 14
DEBUG_MESSAGE = 99

#
# Server <-> Client
#

UPDATE_TEXT = 20 # <A/D>:row:col:text

headers = [INTRODUCTION,
           REQUEST_DOCUMENT_LIST,
           DOCUMENT_REQUEST,
           REQUEST_RESPONSE,
           REQUEST_NOT_OK,
           RESPOND_DOCUMENT_LIST,
           UPDATE_TEXT,
           DEBUG_MESSAGE]


def construct_header(header, payload_len):
    ret_header = PACKET_START
    ret_header += HEADER_FIELD_SEPARATOR
    ret_header += format(header, '02d')
    ret_header += HEADER_FIELD_SEPARATOR
    ret_header += format(payload_len, '03d')
    ret_header += HEADER_FIELD_SEPARATOR

    return ret_header


def check_header(header):
    parts = header.split(HEADER_FIELD_SEPARATOR)
    if len(parts) != 4:
        return False

    if len(parts[1]) != 2:
        return False

    if len(parts[2]) != 3:
        return False

    return True
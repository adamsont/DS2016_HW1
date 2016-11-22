__author__ = 'Taavi'

import common.protocol as P
import logging


#
# Client -> Server
#

class IntroductionPacket:
    def __init__(self, c_name=''):
        self.c_name = c_name

    def serialize(self):
        payload = self.c_name
        header = P.construct_header(P.INTRODUCTION, len(payload))

        return header + payload

    @staticmethod
    def try_parse(header, payload):
        if header != P.INTRODUCTION:
            return None

        c_id = payload
        packet = IntroductionPacket(c_id)
        return packet


class DocumentRequestPacket:
    def __init__(self, file_name):
        self.file_name = file_name

    def serialize(self):
        payload = self.file_name
        header = P.construct_header(P.DOCUMENT_REQUEST, len(payload))

        return header + payload

    @staticmethod
    def try_parse(header, payload):
        if header != P.DOCUMENT_REQUEST:
            return None

        file_name = payload
        packet = DocumentRequestPacket(file_name)
        return packet


#
# Client <-> Server
#

class UpdateTextPacket:
    def __init__(self, option='A', row_start=0, row_end=0, text=''):
        self.option = option
        self.row_start = row_start
        self.row_end = row_end
        self.text = text

    def serialize(self):
        payload = self.option
        payload += P.PAYLOAD_FIELD_SEPARATOR
        payload += str(self.row_start)
        payload += P.PAYLOAD_FIELD_SEPARATOR
        payload += str(self.row_end)
        payload += P.PAYLOAD_FIELD_SEPARATOR
        payload += self.text

        header = P.construct_header(P.UPDATE_TEXT, len(payload))

        return header + payload

    @staticmethod
    def try_parse(header, payload):
        parts = payload.split(P.PAYLOAD_FIELD_SEPARATOR)

        if header != P.UPDATE_TEXT:
            return None

        if len(parts) < 4:
            return None

        option = parts[0]
        row_start = int(parts[1])
        row_end = int(parts[2])
        text = P.PAYLOAD_FIELD_SEPARATOR.join(parts[3:])

        packet = UpdateTextPacket(option,row_start,row_end,text)
        return packet

#
# Server -> Client
#


class RequestResponsePacket:
    RESPONSE_OK = 'Y'
    RESPONSE_NOT_OK = 'N'

    def __init__(self, response):
        self.response = response

    def serialize(self):
        payload = str(self.response)
        header = P.construct_header(P.REQUEST_RESPONSE, len(payload))
        return header + payload

    @staticmethod
    def try_parse(header, payload):
        if header != P.REQUEST_RESPONSE:
            return None

        response = payload
        packet = RequestResponsePacket(response)
        return packet


class DocumentSendPacket:
    def __init__(self, chunk_id, total_chunks, chunk):
        self.chunk_id = chunk_id
        self.total_chunks = total_chunks
        self.chunk = chunk

    def serialize(self):
        payload = str(self.chunk_id)
        payload += P.PAYLOAD_FIELD_SEPARATOR
        payload += str(self.total_chunks)
        payload += P.PAYLOAD_FIELD_SEPARATOR
        payload += self.chunk

        header = P.construct_header(P.DOCUMENT_DOWNLOAD, len(payload))

        return header + payload

    @staticmethod
    def try_parse(header, payload):
        if header != P.DOCUMENT_DOWNLOAD:
            return None

        parts = payload.split(P.PAYLOAD_FIELD_SEPARATOR)

        if len(parts) < 3:
            return None

        chunk_id = int(parts[0])
        total_chunks = int(parts[1])
        chunk = P.PAYLOAD_FIELD_SEPARATOR.join(parts[2:])

        packet = DocumentSendPacket(chunk_id, total_chunks, chunk)
        return packet




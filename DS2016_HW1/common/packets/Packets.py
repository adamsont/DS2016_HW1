__author__ = 'Taavi'

import common.protocol as P
import logging

class UpdateTextPacket:
    def __init__(self, option='A', row=0, column=0, text=''):
        self.option = option
        self.row = row
        self.column = column
        self.text = text

    def serialize(self):
        payload = self.option
        payload += P.PAYLOAD_FIELD_SEPARATOR
        payload += str(self.row)
        payload += P.PAYLOAD_FIELD_SEPARATOR
        payload += str(self.column)
        payload += P.PAYLOAD_FIELD_SEPARATOR
        payload += self.text

        header = P.compose_header(P.UPDATE_TEXT, len(payload))

        return header + payload

    @staticmethod
    def try_parse(header, payload):
        parts = payload.split(P.PAYLOAD_FIELD_SEPARATOR)

        if header != P.UPDATE_TEXT:
            return None

        if len(parts) < 4:
            return None

        option = parts[0]
        row = int(parts[1])
        col = int(parts[2])
        text = P.PAYLOAD_FIELD_SEPARATOR.join(parts[3:])

        packet = UpdateTextPacket(option,row,col,text)
        return packet


class IntroductionPacket:
    def __init__(self, c_id=''):
        self.c_id = c_id

    def serialize(self):
        payload = self.c_id
        header = P.compose_header(P.INTRODUCTION, len(payload))

        return header + payload

    @staticmethod
    def try_parse(header, payload):
        if header != P.INTRODUCTION:
            logging.info("Not introductionpacket header")
            return None

        c_id = payload
        packet = IntroductionPacket(c_id)
        return packet
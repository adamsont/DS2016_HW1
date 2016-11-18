__author__ = 'Taavi'

import common.protocol as P
import logging

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
        row_start = int(parts[1])
        row_end = int(parts[2])
        text = P.PAYLOAD_FIELD_SEPARATOR.join(parts[3:])

        packet = UpdateTextPacket(option,row_start,row_end,text)
        return packet


class IntroductionPacket:
    def __init__(self, c_name=''):
        self.c_name = c_name

    def serialize(self):
        payload = self.c_name
        header = P.compose_header(P.INTRODUCTION, len(payload))

        return header + payload

    @staticmethod
    def try_parse(header, payload):
        if header != P.INTRODUCTION:
            return None

        c_id = payload
        packet = IntroductionPacket(c_id)
        return packet
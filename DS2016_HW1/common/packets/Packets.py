__author__ = 'Taavi'

import common.protocol as P


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
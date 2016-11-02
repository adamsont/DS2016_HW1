__author__ = 'Taavi'

import common.Protocol as P


class UpdateTextPacket:
    def __init__(self, add_delete, row, column, text):
        self.add_delete = add_delete
        self.row = row
        self.column = column
        self.text = text

    def serialize(self):
        payload = self.add_delete
        payload += P.PAYLOAD_FIELD_SEPARATOR
        payload += str(self.row)
        payload += P.PAYLOAD_FIELD_SEPARATOR
        payload += str(self.column)
        payload += P.PAYLOAD_FIELD_SEPARATOR
        payload += self.text

        header = P.compose_header(P.UPDATE_TEXT, len(payload))

        return header + payload
__author__ = 'Taavi'

from common.utilities.actor import *
from common.packets.packets import *


class CollaborationGroup(Actor):
    def __init__(self):
        Actor.__init__(self)

        self.collaborators = []
        self.start()

    def add_collaborator(self, connection):
        logging.info("Adding new collaborator")
        self.collaborators.append(connection)
        connection.on_update_text_delegate = self.on_update_text

    def tick(self):
        pass

    def on_update_text(self, c_id, option, row, col, text):
        self.message_queue.put(lambda: self.on_update_text_handler(c_id, option, row, col, text))

    def on_update_text_handler(self, c_id, option, row, col, text):
        logging.info("Collaborator " + str(c_id) + " changed text")

        for collaborator in self.collaborators:
            if collaborator.get_cid() != c_id:
                packet = UpdateTextPacket(option, row, col, text)
                collaborator.send_packet(packet)
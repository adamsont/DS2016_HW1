__author__ = 'Taavi'

from common.utilities.actor import *
from common.packets.packets import *


class CollaborationGroup(Actor):
    def __init__(self):
        Actor.__init__(self)

        self.collaborators = []
        self.start()

    def add_collaborator(self, connection):
        self.message_queue.put(lambda: self.add_collaborator_handler(connection))

    def tick(self):
        pass

    #
    # PUBLIC
    #

    def on_update_text(self, c_id, packet):
        self.message_queue.put(lambda: self.on_update_text_handler(c_id, packet))

    def on_collaborator_lost(self, c_id):
        self.message_queue.put(lambda: self.on_collaborator_lost_handler(c_id))

    def on_document_received(self, c_id, text):
        self.message_queue.put(lambda: self.on_document_received_handler(c_id, text))
    #
    # PRIVATE
    #

    def add_collaborator_handler(self, connection):
        logging.info("Adding new collaborator")
        self.collaborators.append(connection)
        connection.on_update_text_delegate = self.on_update_text
        connection.on_connection_lost_delegate = self.on_collaborator_lost
        connection.on_document_received_delegate = self.on_document_received

    def on_collaborator_lost_handler(self, c_id):
        for c in self.collaborators:
            if c.get_cid() == c_id:
                self.collaborators.remove(c)
                break

    def on_update_text_handler(self, c_id, packet):
        pass
        #logging.info("Collaborator " + str(c_id) + " changed text")

        #for collaborator in self.collaborators:
         #   if collaborator.get_cid() != c_id:
           #     collaborator.send_packet(packet)

    def on_document_received_handler(self, c_id, text):
        logging.info("Collaborator " + str(c_id) + " changed text")
        logging.info(text)

        for collaborator in self.collaborators:
            if collaborator.get_cid() != c_id:
                collaborator.send_document(text)
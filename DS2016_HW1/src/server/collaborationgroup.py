__author__ = 'Taavi'

from common.utilities.actor import *
from common.packets.packets import *


class CollaborationGroup(Actor):
    def __init__(self, f):
        Actor.__init__(self)

        self.collaboration_file = f
        self.collaborators = []
        self.current_text = self.collaboration_file.read()
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

    def on_document_requested(self, c_id, file_name):
        self.message_queue.put(lambda: self.on_document_requested_handler(c_id, file_name))

    #
    # PRIVATE
    #

    def add_collaborator_handler(self, connection):
        logging.info("Adding new collaborator")
        self.collaborators.append(connection)
        connection.on_update_text_delegate = self.on_update_text
        connection.on_connection_lost_delegate = self.on_collaborator_lost
        connection.on_document_received_delegate = self.on_document_received
        connection.on_document_requested_delegate = self.on_document_requested

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

        self.current_text = text
        self.collaboration_file.seek(0)
        self.collaboration_file.truncate()
        self.collaboration_file.write(self.current_text)
        self.collaboration_file.flush()

        for collaborator in self.collaborators:
            if collaborator.get_cid() != c_id:
                collaborator.send_document(text)

    def on_document_requested_handler(self, c_id, file_name):
        logging.info("Client: " + str(c_id) + " requested document: " + file_name)
        requester = self.get_collaborator_by_id(c_id)

        if file_name == 'correct':
            rrp = RequestResponsePacket(RequestResponsePacket.RESPONSE_OK)
            requester.send_packet(rrp)
            requester.send_document(self.current_text)
        else:
            rrp = RequestResponsePacket('N')
            requester.send_packet(rrp)

    def get_collaborator_by_id(self, c_id):
        for collaborator in self.collaborators:
            if collaborator.get_cid() == c_id:
                return collaborator

        return None
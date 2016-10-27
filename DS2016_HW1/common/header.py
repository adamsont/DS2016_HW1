__author__ = 'Taavi'

#
# Headers just flipping around in the breeze since Python 2.7 does not have any enums...
#

#
# Client -> Server
#

INTRODUCTION = 1
REQUEST_DOCUMENT_LIST = 2
REQUEST_UPDATE = 3

#
# Server -> Client
#

CONFIRMATION = 11
RESPOND_DOCUMENT_LIST = 12
RESPOND_UPDATE = 13

#
# Server <-> Client
#

UPDATE_TEXT_DELETED = 20
UPDATE_TEXT_ADDED = 21
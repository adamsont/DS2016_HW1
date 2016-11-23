__author__ = 'Taavi'

import Tkinter as Tk
import Queue
import logging


import common.protocol as P

import common.utilities.utilities as util
import client_actor
import TestThread

class Application(Tk.Frame):

    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.grid()

        self.master.title("Client App as Unknown")
        master.geometry('{}x{}'.format(1100, 600))
        #
        # Variables
        #
        self.msg_queue = Queue.Queue()
        self.last_text = list()
        self.name_var = Tk.StringVar()
        self.name_var.set('Unknown')
        self.initialized = False
        self.introduced = False

        #
        #Widgets
        #
        self.text_box = None
        self.set_name_button = None
        self.name_entry = None

        self.create_widgets()
        self.inner_loop()

        self.connection = client_actor.ClientActor(P.SERVER_HOST, P.SERVER_PORT)
        self.connection.on_update_text_delegate = self.process_update_text
        self.connection.on_document_delegate = self.process_new_document
        self.connection.on_connected_delegate = self.initialize
        self.connection.on_connection_lost_delegate = self.on_connection_lost

    # Handles all requests from another threads and runs them in its own
    def inner_loop(self):
        try:
            f = self.msg_queue.get(False)
            f()
        except Queue.Empty:
            pass

        self.master.after(10, self.inner_loop)

    def create_widgets(self):
        master_frame = Tk.Frame(self)

        self.name_entry = Tk.Entry(master_frame, textvariable=self.name_var)
        self.name_entry.config(state=Tk.DISABLED)
        self.name_entry.pack(padx=5, pady=0, side=Tk.LEFT, anchor="nw")

        self.set_name_button = Tk.Button(master_frame, text="Set name", command=self.set_name)
        self.set_name_button.pack(padx=5, pady=0, side=Tk.LEFT, anchor="nw")

        self.text_box = Tk.Text(master_frame, width=100, height=1000)
        self.text_box.bind("<KeyRelease>", self.on_text_changed_handler)
        self.text_box.pack(side=Tk.TOP)
        self.text_box.config(state=Tk.DISABLED)

        self.last_text = list(unicode(self.text_box.get("1.0", Tk.END)))
        self.last_text.pop()
        master_frame.pack()

    def on_text_changed_handler(self, event):
        if not self.initialized or not self.introduced:
            return

        current_text = str(self.text_box.get("1.0", Tk.END))
        #current_text = current_text[:-1]

        self.connection.send_document(current_text)
        return
        # Deleting is just adding the other way around :D

        #change = len(current_text) - len(self.last_text)
#
        #if change == 0:
        #    return
#
        ##logging.debug("Curr: " + unicode(current_text))
        ##logging.debug("Last: " + unicode(self.last_text))
#
        #if len(current_text) < len(self.last_text):
        #    logging.debug("Deleted " + str(change))
        #    diff, row, col = util.find_changes(self.last_text, current_text)
#
        #    report_row = max(row - 1, 1)
        #    report_row2 = report_row + diff.count('\n') + 2
#
        #    changed_text = unicode(self.text_box.get(str(report_row)+".0", str(report_row2 + 1)+".0"))
        #    changed_text = changed_text[:-1]
#
        #    logging.info("Text removed, reporting rows: " + str(report_row) + ":" + str(report_row2) + " with text:\n" + changed_text)
        #    self.report_change('D', report_row, report_row2, changed_text)
#
        #else:
        #    logging.debug("Added " + str(change))
        #    diff, row, col = util.find_changes(current_text, self.last_text)
#
        #    report_row = max(row - 1, 1)
        #    report_row2 = report_row + diff.count('\n') + 2
#
        #    changed_text = unicode(self.text_box.get(str(report_row)+".0", str(report_row2 + 1)+".0"))
        #    changed_text = changed_text[:-1]
#
        #    logging.info("Text added, reporting rows: " + str(report_row) + ":" + str(report_row2) + " with text:\n" + changed_text)
        #    self.report_change('A', report_row, report_row2, changed_text)
#
        #logging.debug(diff + " at: " + str(row) + "." + str(col))
        #self.last_text = current_text

    def report_change(self, option, row, col, text):
        self.connection.send_text_update(option, row, col, text)

    #
    # PRIVATE
    #

    def on_text_changed(self, event):
        self.msg_queue.put(lambda: self.on_text_changed_handler(event))

    def add_text(self, row_start, row_end, text):
        logging.info('Adding text: ' + text + " at " + str(int(row_start))+':'+str(int(row_end)))
        #self.on_text_changed_handler(None)

        current_text = str(self.text_box.get('1.0', Tk.END))
        current_text = util.replace_text(current_text, text, row_start, row_end)

        self.set_text(current_text)

    def remove_text(self, row_start, row_end, text):
        logging.info('Removing text: ' + text + " at " + str(int(row_start))+':'+str(int(row_end)))
        current_text = str(self.text_box.get('1.0', Tk.END))
        current_text = util.delete_text(current_text, row_start, row_end)

        #del_parts = text.split('\n')
        #l_row = row
        #l_col = col
#
        #for part in del_parts:
        #    self.text_box.delete(str(int(l_row))+'.'+str(int(l_col)), str(int(l_row))+'.'+str(int(l_col)+len(part)))
        #    l_row += 1
        #    l_col = 0
#
        #self.on_text_changed_handler(None)
        #self.text_box.delete(str(int(row))+'.'+str(int(col)), str(int(row))+'.'+str(int(col)+len(text)))
        self.set_text(current_text)

    def set_name(self):
        if self.introduced:
            return

        if self.initialized:
            self.name_entry.config(state=Tk.DISABLED)
            self.text_box.config(state=Tk.NORMAL)
            self.connection.introduce(self.name_var.get())
            self.master.title("Client App as " + self.name_var.get())
            self.introduced = True

    def process_update_text_handler(self, packet):
        if packet.option == 'A':
            self.add_text(packet.row_start, packet.row_end, packet.text)
        elif packet.option == 'D':
            self.remove_text(packet.row_start, packet.row_end, packet.text)
        else:
            logging.info("Unknown text update option")

    def process_new_document_handler(self, text):
        logging.info("Setting text: " + text)
        self.set_text(text)

    def set_text(self, text):
        self.text_box.delete('1.0', Tk.END)
        self.text_box.insert('1.0', text)
        self.last_text = list(unicode(self.text_box.get("1.0", Tk.END)))
        self.last_text.pop()

    def initialize_handler(self):
        self.name_entry.config(state=Tk.NORMAL)
        self.initialized = True

    def on_connection_lost_handler(self):
        self.text_box.config(state=Tk.DISABLED)
        self.introduced = False
        self.initialized = False
    #
    # PUBLIC
    #
    def initialize(self):
        self.msg_queue.put(lambda: self.initialize_handler())

    def process_update_text(self, packet):
        self.msg_queue.put(lambda: self.process_update_text_handler(packet))

    def process_new_document(self, text):
        self.msg_queue.put(lambda: self.process_new_document_handler(text))

    def on_connection_lost(self):
        self.msg_queue.put(lambda: self.on_connection_lost_handler())

logging.basicConfig(level=logging.DEBUG)
root = Tk.Tk()

app = Application(master=root)

app.mainloop()



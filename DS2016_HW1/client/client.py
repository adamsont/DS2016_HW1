__author__ = 'Taavi'

import Tkinter as Tk
import Queue
import logging

import common.protocol as P

import common.utilities.Utilities as util
import connectionactor
import TestThread


class Application(Tk.Frame):

    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.grid()
        self.master.title("Client App")
        master.geometry('{}x{}'.format(800, 600))
        #
        # Variables
        #
        self.msg_queue = Queue.Queue()
        self.last_text = list()
        #
        #Widgets
        #
        self.text_box = None
        self.test_button = None

        self.create_widgets()
        self.inner_loop()

        self.connection = connectionactor.ConnectionActor(P.SERVER_HOST, P.SERVER_PORT)
        self.connection.sub_on_update_text(self.process_update_text)

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

        self.test_button = Tk.Button(master_frame, text="Test", command=self.test)
        self.test_button.pack(padx=5, pady=0, side=Tk.LEFT, anchor="nw")

        self.text_box = Tk.Text(master_frame, width=100, height=1000)
        self.text_box.insert(Tk.END, "Texst")
        self.text_box.bind("<KeyRelease>", self.on_text_changed_handler)
        self.text_box.pack(side=Tk.TOP)

        self.last_text = list(unicode(self.text_box.get("1.0", Tk.END)))
        self.last_text.pop()
        master_frame.pack()

    def on_text_changed_handler(self, event):
        current_text = list(unicode(self.text_box.get("1.0", Tk.END)))
        current_text.pop()

        # Deleting is just adding the other way around :D

        change = len(current_text) - len(self.last_text)

        if change == 0:
            return

        #logging.debug("Curr: " + unicode(current_text))
        #logging.debug("Last: " + unicode(self.last_text))

        if len(current_text) < len(self.last_text):
            logging.debug("Deleted " + str(change))
            diff, row, col = util.find_changes(self.last_text, current_text)
            # Report delete
            self.report_change('D', row, col, diff)
        else:
            logging.debug("Added " + str(change))
            diff, row, col = util.find_changes(current_text, self.last_text)
            # Report addition
            self.report_change('A', row, col, diff)

        logging.debug(diff + " at: " + str(row) + "." + str(col))
        self.last_text = current_text

    def report_change(self, option, row, col, text):
        self.connection.send_text_update(option, row, col, text)

    #
    # Private functions
    #

    def on_text_changed(self, event):
        self.msg_queue.put(lambda: self.on_text_changed_handler(event))

    def add_text(self, row, col, text):
        logging.info('Adding text: ' + text + " at " + str(int(row))+'.'+str(int(col)))
        self.on_text_changed_handler(None)
        self.text_box.insert(str(int(row))+'.'+str(int(col)), text)
        self.last_text = list(unicode(self.text_box.get("1.0", Tk.END)))
        self.last_text.pop()

    def remove_text(self, row, col, text):
        logging.info('Removing text: ' + text + " at " + str(int(row))+'.'+str(int(col)) + " - " + str(int(row))+'.'+str(int(col)+len(text)))

        del_parts = text.split('\n')
        l_row = row
        l_col = col

        for part in del_parts:
            self.text_box.delete(str(int(l_row))+'.'+str(int(l_col)), str(int(l_row))+'.'+str(int(l_col)+len(part)))
            l_row += 1
            l_col = 0

        self.on_text_changed_handler(None)
        self.text_box.delete(str(int(row))+'.'+str(int(col)), str(int(row))+'.'+str(int(col)+len(text)))
        self.last_text = list(unicode(self.text_box.get("1.0", Tk.END)))
        self.last_text.pop()

    def test(self):
        self.text_box.delete('1.3', '1.6')
        self.last_text = list(unicode(self.text_box.get("1.0", Tk.END)))

    def process_update_text_handler(self, option, row, col, text):
        if option == 'A':
            self.add_text(row, col, text)
        elif option == 'D':
            self.remove_text(row, col, text)
        else:
            logging.info("Unknown text update option")

    #
    # Public functions, add messages to the queue
    #

    def process_update_text(self, option, row, col, text):
        self.msg_queue.put(lambda: self.process_update_text_handler(option, row, col, text))


logging.basicConfig(level=logging.DEBUG)

root = Tk.Tk()
app = Application(master=root)

#t = TestThread.TestThread(app.pr, "ABC")
#t.start()


app.mainloop()



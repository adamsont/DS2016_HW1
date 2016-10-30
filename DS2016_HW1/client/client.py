__author__ = 'Taavi'

import Tkinter as Tk
import Queue
import logging

import common.protocol as P

import common.utilities.utilities as util
import clientconnection
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

        self.text_box = Tk.Text(master_frame, width=1000, height=1000)
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
            diff, final_row, final_col = util.find_changes(self.last_text, current_text)
            # Report delete
        else:
            logging.debug("Added " + str(change))
            diff, final_row, final_col = util.find_changes(current_text, self.last_text)
            # Report addition

        logging.debug(diff + " at: " + str(final_row) + "." + str(final_col))
        self.last_text = current_text
    #
    # Private functions
    #
    def on_text_changed(self, event):
        self.msg_queue.put(lambda: self.on_text_changed_handler(event))

    def add_text_handler(self, row, col, text):
        self.on_text_changed_handler(None)
        self.text_box.insert(str(int(row))+'.'+str(int(col)), text)
        self.last_text = list(unicode(self.text_box.get("1.0", Tk.END)))
        self.last_text.pop()

    def test(self):
        self.text_box.insert("1.3", "CHANGE")
        self.last_text = list(unicode(self.text_box.get("1.0", Tk.END)))
    #
    # Public functions, add messages to the queue
    #

    def add_text(self, text):
        self.msg_queue.put(lambda: self.add_text_handler(1, 5, text))



logging.basicConfig(level=logging.DEBUG)

root = Tk.Tk()
app = Application(master=root)

t = TestThread.TestThread(app.add_text, "ABC")
t.start()

connection = clientconnection.ClientConnection(P.SERVER_HOST, P.SERVER_PORT)


app.mainloop()

connection.terminate()



__author__ = 'Taavi'

import threading
import time
import Tkinter as Tk
import tkFileDialog
import Queue
import logging
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

    def inner_loop(self):
        try:
            f = self.msg_queue.get(False)
            f()
        except Queue.Empty:
            pass

        self.master.after(100, self.inner_loop)

    def create_widgets(self):
        master_frame = Tk.Frame(self)

        self.test_button = Tk.Button(master_frame, text="Test", command=self.test)
        self.test_button.pack(padx=5, pady=0, side=Tk.LEFT, anchor="nw")

        self.text_box = Tk.Text(master_frame, width=1000, height=1000)
        self.text_box.insert(Tk.END, "Texst")
        self.text_box.bind("<KeyRelease>", self.text_changed)
        self.text_box.pack(side=Tk.TOP)



        self.last_text = list(unicode(self.text_box.get("1.0", Tk.END)))
        master_frame.pack()

    def text_changed(self, event):
        current_text = list(unicode(self.text_box.get("1.0", Tk.END)))
        #logging.debug("Curr: " + unicode(current_text))
        #logging.debug("Last: " + unicode(self.last_text))

        row = 1
        col = 0

        for i in range(len(current_text) - 1):
            col += 1

            if current_text[i] == '\n':
                row += 1
                col = 0

            if current_text[i] != self.last_text[i]:
                #logging.debug("New char: " + unicode(current_text[i]))
                logging.debug(unicode(current_text[i]+ ' ' + str(row) + ":" + str(col - 1)))
                break



        #print unicode(self.text_box.get("1.0", Tk.END))
        self.last_text = current_text
    #
    # Private functions
    #

    def add_text(self, text):
        self.text_box.insert(Tk.END, text)

    def test(self):
        self.text_box.insert("1.3", "CHANGE")
        self.last_text = list(unicode(self.text_box.get("1.0", Tk.END)))
    #
    # Public functions, add messages to the queue
    #

    def add_message(self, text):
        logging.info("add_message")
        self.msg_queue.put(lambda: self.add_text(text))



logging.basicConfig(level=logging.DEBUG)
root = Tk.Tk()
app = Application(master=root)

#t = TestThread.TestThread(app.add_message, "Tekst")
#t.start()

logging.info("THREAD CREATED")
app.mainloop()



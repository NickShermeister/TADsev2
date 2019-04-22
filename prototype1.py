#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
First prototpye of TADse's application.
"""

from tkinter import Tk, BOTH, Label, TOP, YES
from tkinter.ttk import Frame, Button, Style
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename

import os
dir_path = os.path.dirname(os.path.realpath(__file__)) # + "/../.."

WIDTH = 1200
HEIGHT = 1200
LARGE_FONT = ("Verdana", 12)


class BaseTK(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)

        container.pack(sid="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # for F in (DataRequestF, BasicDataF): #, PaceDataF, PullDataF, ComparisonDataF):
        print("Hi")
        frame = DataRequestF(container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        self.frames[DataRequestF] = frame

        self.show_frame(DataRequestF)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class DataRequestF(Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.style = Style()
        self.style.theme_use("default")
        # self.master.title("Seeing Eye Data Viewing Application")
        self.pack(fill=BOTH, expand=1)

        quitButton = Button(self, text="Quit", command=self.quit)
        importButton = Button(self, text="Import Data", command=lambda: importInfo())

        # imageFile = "test.jpg"
        # tempImage = Image.open(imageFile)

        # get the image size
        # w = tempImage.width
        # h = tempImage.height
        # print("w: %d \n h: %d \n" % (w, h))

        # tempImage = tempImage.resize((int (w/2), int (h/2) ), Image.ANTIALIAS)

        # self.image1 = ImageTk.PhotoImage(tempImage)

        # position coordinates of root 'upper left corner'
        # x1 = 0
        # y1 = 0
        x = 0
        y = 0


        quitButton.place(x=(WIDTH/2), y=(HEIGHT*3/4))

        importButton.place(x=(WIDTH/2), y=(HEIGHT/4 - 50))

        # root has no image argument, so use a label as a panel
        # self.panel1 = Label(self.master, image=self.image1)
        # self.display = self.image1

        # self.panel1.place(x=(w/4), y=(h/4))
        # self.panel1.pack(side=TOP, fill=BOTH, expand=YES)
        print ("Info prompt screen")


class BasicDataF(Frame):

    def __init__(self, parent, controller):
        super().__init__()

        self.style = Style()
        self.style.theme_use("default")
        # self.master.title("Seeing Eye Data Viewing Application")
        self.pack(fill=BOTH, expand=1)

        quitButton = Button(self, text="Quit", command=self.quit)
        importButton = Button(self, text="Import Data", command=lambda: importInfo())

        # imageFile = "test.jpg"
        # tempImage = Image.open(imageFile)

        # get the image size
        # w = tempImage.width
        # h = tempImage.height
        # print("w: %d \n h: %d \n" % (w, h))

        # tempImage = tempImage.resize((int (w/2), int (h/2) ), Image.ANTIALIAS)

        # self.image1 = ImageTk.PhotoImage(tempImage)

        # position coordinates of root 'upper left corner'
        # x1 = 0
        # y1 = 0
        x = 0
        y = 0


        quitButton.place(x=(WIDTH/2), y=(HEIGHT*3/4))

        importButton.place(x=(WIDTH/2), y=(HEIGHT/4 - 50))

        # root has no image argument, so use a label as a panel
        # self.panel1 = Label(self.master, image=self.image1)
        # self.display = self.image1

        # self.panel1.place(x=(w/4), y=(h/4))
        # self.panel1.pack(side=TOP, fill=BOTH, expand=YES)
        print ("Info prompt screen")

class PaceDataF(Frame):

    def __init__(self, parent, controller):
        super().__init__()

        self.initUI(parent, controller)

    def initUI(self, parent, controller):
        pass

class PullDataF(Frame):

    def __init__(self, parent, controller):
        super().__init__()

        self.initUI(parent, controller)

    def initUI(self, parent, controller):
        pass

class ComparisonDataF(Frame):

    def __init__(self, parent, controller):
        super().__init__()

        self.initUI(parent, controller)

    def initUI(self, parent, controller):
        pass



def main():
    root = BaseTK()
    # root.geometry("250x150+300+300")
    # app = DataRequestF()
    root.mainloop()

def importInfo():
    filename = askopenfilename(initialdir = dir_path,title = "Select file") # show an "Open" dialog box and return the path to the selected file
    print(filename)
    root.show_frame(BasicDataF)


if __name__ == '__main__':
    main()

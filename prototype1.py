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

WIDTH = 1500
HEIGHT = 1500
LARGE_FONT = ("Verdana", 12)


def importInfo(basetk):
    filename = askopenfilename(initialdir = dir_path,title = "Select file") # show an "Open" dialog box and return the path to the selected file
    print(filename)
    basetk.show_frame(BasicDataF)

class BaseTK(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)

        container.pack(sid="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class DataRequestF(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.style = Style()
        self.style.theme_use("default")

        self.master.title("Quit button")
        self.pack(fill=BOTH, expand=1)

        quitButton = Button(self, text="Quit", command=self.quit)
        importButton = Button(self, text="Import Data", command=importInfo)

        imageFile = "test.jpg"
        tempImage = Image.open(imageFile)

        # get the image size
        w = tempImage.width
        h = tempImage.height
        print("w: %d \n h: %d \n" % (w, h))

        tempImage = tempImage.resize((int (w/2), int (h/2) ), Image.ANTIALIAS)

        self.image1 = ImageTk.PhotoImage(tempImage)

        # position coordinates of root 'upper left corner'
        x1 = 0
        y1 = 0
        x = 0
        y = 0

        # make the root window the size of the image
        self.master.geometry("%dx%d+%d+%d" % (WIDTH, HEIGHT, x, y))

        quitButton.place(x=(w/2), y=(h*3/4))

        importButton.place(x=(w/2), y=(h/4 - 50))

        # root has no image argument, so use a label as a panel
        self.panel1 = Label(self.master, image=self.image1)
        self.display = self.image1

        self.panel1.place(x=(w/4), y=(h/4))
        # self.panel1.pack(side=TOP, fill=BOTH, expand=YES)
        print ("Display image1")


class BasicDataF(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        pass

class PaceDataF(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        pass

class PullDataF(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        pass

class ComparisonDataF(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        pass



def main():
    root = Tk()
    root.geometry("250x150+300+300")
    app = DataRequestF()
    root.mainloop()


if __name__ == '__main__':
    main()

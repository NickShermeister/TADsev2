#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

This program creates a Quit
button. When we press the button,
the application terminates.

Author: Jan Bodnar
Last modified: July 2017
Website: www.zetcode.com
"""

from tkinter import Tk, BOTH, Label, TOP, YES
from tkinter.ttk import Frame, Button, Style
from PIL import Image, ImageTk

class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.style = Style()
        self.style.theme_use("default")

        self.master.title("Quit button")
        self.pack(fill=BOTH, expand=1)

        quitButton = Button(self, text="Quit", command=self.quit)


        imageFile = "test.jpg"
        self.image1 = ImageTk.PhotoImage(Image.open(imageFile))

        # get the image size
        w = self.image1.width()*2
        h = self.image1.height()*2
        print("w: %d \n h: %d \n" % (w, h))

        # position coordinates of root 'upper left corner'
        x1 = 0
        y1 = 0
        x = 0
        y = 0

        # make the root window the size of the image
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))

        quitButton.place(x=(w/2), y=(h*3/4))

        # root has no image argument, so use a label as a panel
        self.panel1 = Label(self.master, image=self.image1)
        self.display = self.image1

        self.panel1.place(x=(w/4), y=(h/4))
        # self.panel1.pack(side=TOP, fill=BOTH, expand=YES)
        print ("Display image1")


class OpeningPrompt(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        pass

class BasicData(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        pass







def main():

    root = Tk()
    root.geometry("250x150+300+300")
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()

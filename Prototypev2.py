from tkinter import Tk, BOTH, Label, TOP, YES
from tkinter.ttk import Frame, Button, Style
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
# import csv
import pandas as pd
import matplotlib
matplotlib.use("TkAgg") #it's the backend of matplotlib

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import os
dir_path = os.path.dirname(os.path.realpath(__file__)) # + "/../.."


LARGE_FONT = ("Verdana", 12)
HEIGHT = 1000
WIDTH = 1000

# dataIn = 0;
fileloc = "test_values.csv"

class containerClass(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)

        container.pack(sid="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        geometryString = str(HEIGHT) + "x" + str(WIDTH)
        self.geometry(geometryString)

        self.frames = {}

        for F in (DataImportF, BasicDataF):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame


        self.show_frame(DataImportF)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class DataImportF(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Data Import Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = Button(self, text="Import Pace & Pull Data", command=lambda: self.importInfo(controller))
        button1.pack(pady=HEIGHT/3)

        # button2 = Button(self, text="Import Pace Data (coming soon)")#, command=lambda: controller.show_frame(PageOne))
        # button2.pack()
        #
        # button3 = Button(self, text="Import Pull Data (coming soon)")#, command=lambda: controller.show_frame(PageOne))
        # button3.pack()

    def importInfo(self, controller):
        filename = askopenfilename(initialdir = dir_path,title = "Select file") # show an "Open" dialog box and return the path to the selected file
        print(filename)
        fileloc = filename


        controller.show_frame(BasicDataF)

class BasicDataF(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Basic Data Information", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        dataIn = pd.read_csv(fileloc)
        print(dataIn)
        first = dataIn.loc["First"]
        second = dataIn.loc["Second"]
        a.plot([1,2,3,4,5,6,7,8],[1,2,3,4,5,6,7,8])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

class PaceDataF(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Page 1", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()


app = containerClass()
app.mainloop()

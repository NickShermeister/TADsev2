from tkinter import Tk, BOTH, Label, TOP, YES, Text, END
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

dataIn = 0
fileloc = 0

# When re-importing data, just completely destroy then re-create with the new data


class containerClass(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, None, None)
        container = Frame(self)

        # self.dataIn = args[0]
        container.pack(sid="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        geometryString = str(HEIGHT) + "x" + str(WIDTH)
        self.geometry(geometryString)

        self.frames = {}

        for F in (DataImportF, BasicDataF, PaceDataF):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame
        
        self.show_frame(DataImportF)

    def requestInfo(self):
        global dataIn
        global fileloc
        filename = askopenfilename(initialdir = dir_path,title = "Select file") # show an "Open" dialog box and return the path to the selected file
        print(filename)
        fileloc = filename
        dataIn = pd.read_csv(fileloc)
        self.show_frame(BasicDataF)

    def show_frame(self, cont):
        frame = self.frames[cont]
        if(cont == PaceDataF):
            frame.update_plot()
        frame.tkraise()
        if(cont == BasicDataF):
            frame.calcInfo()

class DataImportF(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Data Import Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = Button(self, text="Imported Pace & Pull Data", command=lambda: controller.requestInfo())
        button1.pack(pady=HEIGHT/3)

        button2 = Button(self, text="Imported Only Pace Data (coming soon)")#, command=lambda: controller.show_frame(PageOne))
        button2.pack()

        button3 = Button(self, text="Imported Only Pull Data (coming soon)")#, command=lambda: controller.show_frame(PageOne))
        button3.pack()

class BasicDataF(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Basic Data Information", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = Button(self, text="Back to Import Page", command=lambda: controller.show_frame(DataImportF))
        button1.pack()

        text1 = Text(self)
        text1.insert(END, "Hello world p1")
        text1.insert(END, "\nHello world p2")

        text1.tag_add("here", "1.0", "1.4")
        text1.tag_config("here", background="yellow", foreground="blue")

        text1.pack()

        button2 = Button(self, text="Go to more pace data", command=lambda: controller.show_frame(PaceDataF))
        button2.pack()

    def calcInfo(self):
        pass

class PaceDataF(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Pace Data", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = Button(self, text="Back to Basic Data", command=lambda: controller.show_frame(BasicDataF))
        button1.pack()


        global dataIn
        self.f = Figure()
        self.a = self.f.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.f, master=self)  # A tk.DrawingArea.
        # self.canvas.draw()



    def update_plot(self):
        # self.canvas.update_plot
        # self.canvas = FigureCanvasTkAgg(self.f, master=self)  # A tk.DrawingArea.
        self.a.clear()
        # self.canvas.delete('all')
        # self.canvas.clear()
        print(dataIn)
        first = list(dataIn['First'])
        second = list(dataIn['Second'])
        print(first)
        print(second)
        self.a.plot(first, second)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)




def main():

    # print(dataIn)
    # plot()
    app = containerClass()
    app.mainloop()


if __name__ == '__main__':
    main()

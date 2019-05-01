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

import numpy as np


DEFAULT_FONT = ("Verdana", 12)
HEIGHT = 1000
WIDTH = 1000

dataIn = 0
fileloc = 0

meanPace = 0
meanPull = 0

paceDistribution = [0, 0, 0, 0, 0]
pullDistribution = [0, 0, 0, 0, 0]

paceProcessed = 0
pullProcessed = 0


firstColumn = "First"
secondColumn = "Second"

upperPercentile = 95
lowerPercentile = 5

mean1 = -1
mean2 = -1

colorDict = {0:"red", 1:"yellow", 2:"green", 3:"yellow", 4:"red"}

paceBorders = [2.0, 2.45, 3.25, 3.95]
pullBorders = [2.5, 5.0, 7.5, 10]

paceBins = [0, 2.0, 2.45, 3.25, 3.95]
pullBins = [0, 2.5, 5.0, 7.5, 10]

paceArea = -1
pullArea = -1

# When re-importing data, just completely destroy then re-create with the new data
def DataCalculations():
    global firstColumn, secondColumn, mean1, mean2, upperPercentile, lowerPercentile, paceDistribution, pullDistribution, paceProcessed, pullProcessed
    global paceBorders, pullBorders, paceArea, pullArea, paceBins, pullBins

    rawPace = np.array(dataIn[firstColumn])
    rawPull = np.array(dataIn[secondColumn])
    paceBins.append(max(rawPace))
    pullBins.append(max(rawPull))

    highBound1 = np.percentile(rawPace, upperPercentile)
    lowBound1 = np.percentile(rawPace, lowerPercentile)
    highBound2 = np.percentile(rawPull, upperPercentile)
    lowBound2 = np.percentile(rawPull, lowerPercentile)

    valid_nums1 = []
    valid_nums2 = []

    for x in rawPace:
        if x <= highBound1 and x >= lowBound1:
            valid_nums1.append(x)
    valid_nums1.sort()

    for x in rawPull:
        if x <= highBound2 and x >= lowBound2:
            valid_nums2.append(x)
    valid_nums2.sort()

    paceProcessed = valid_nums1
    pullProcessed = valid_nums2

    valid_nums1 = np.array(valid_nums1)
    valid_nums2 = np.array(valid_nums2)

    #Means -- let it be of middle 90% of data?
    mean1 = np.mean(valid_nums1)
    mean2 = np.mean(valid_nums2)

    if(mean1 < paceBorders[0]):
        paceArea = 0;
    elif(mean1 < paceBorders[1]):
        paceArea = 1;
    elif(mean1 < paceBorders[2]):
        paceArea = 2;
    elif(mean1 < paceBorders[3]):
        paceArea = 3;
    else:
        paceArea = 4;

    if(mean2 < pullBorders[0]):
        pullArea = 0;
    elif(mean2 < pullBorders[1]):
        pullArea = 1;
    elif(mean2 < pullBorders[2]):
        pullArea = 2;
    elif(mean2 < pullBorders[3]):
        pullArea = 3;
    else:
        pullArea = 4;


    #Distributions -- hardcoded based off of the sheet provided to us by our community partner
    paceDistribution[0] =  len(valid_nums1[ np.where( valid_nums1.all() < 2.0 ) ])
    paceDistribution[1] =  len(valid_nums1[ np.where( valid_nums1.all() < 2.45 and valid_nums1.all() >= 2.0 ) ])
    paceDistribution[2] =  len(valid_nums1[ np.where( valid_nums1.all() < 3.25 and valid_nums1.all() >= 2.45 ) ])
    paceDistribution[3] =  len(valid_nums1[ np.where( valid_nums1.all() < 3.95 and valid_nums1.all() >= 3.25 ) ])
    paceDistribution[4] =  len(valid_nums1[ np.where( valid_nums1.all() >= 3.95 ) ])

    pullDistribution[0] =  len(valid_nums2[ np.where( valid_nums2.all() < 2.5 ) ])
    pullDistribution[1] =  len(valid_nums2[ np.where( valid_nums2.all() < 5 and valid_nums2.all() >= 2.0 ) ])
    pullDistribution[2] =  len(valid_nums2[ np.where( valid_nums2.all() < 7.5 and valid_nums2.all() >= 5 ) ])
    pullDistribution[3] =  len(valid_nums2[ np.where( valid_nums2.all() < 10 and valid_nums2.all() >= 7.5 ) ])
    pullDistribution[4] =  len(valid_nums2[ np.where( valid_nums2.all() >= 10 ) ])


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
            # if F in (PaceDataF, PullDataF):
            #     frame.grid(row=2, column=0, sticky="nsew")
            # else:
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
        DataCalculations()
        self.show_frame(BasicDataF)

    def show_frame(self, cont):
        frame = self.frames[cont]
        # if(cont in [PaceDataF]):
        frame.update()
        frame.tkraise()

class DataImportF(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Data Import Page", font=DEFAULT_FONT)
        label.pack(pady=10,padx=10)

        button1 = Button(self, text="Imported Pace & Pull Data", command=lambda: controller.requestInfo())
        button1.pack(pady=HEIGHT/3)

        button2 = Button(self, text="Imported Only Pace Data (coming soon)")#, command=lambda: controller.show_frame(PageOne))
        button2.pack()

        button3 = Button(self, text="Imported Only Pull Data (coming soon)")#, command=lambda: controller.show_frame(PageOne))
        button3.pack()

    def update(self):
        pass

class BasicDataF(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="Basic Data Information", font=DEFAULT_FONT)
        label.pack(pady=10,padx=10)

        button1 = Button(self, text="Back to Import Page", command=lambda: controller.show_frame(DataImportF))
        button1.pack()

        self.text1 = Text(self, height=32, width=32)
        self.text1.config(width=50, height=5)
        self.text1.pack_propagate(0)
        self.text1.pack()

        button2 = Button(self, text="Go to more pace data", command=lambda: controller.show_frame(PaceDataF))
        button2.pack()

        button3 = Button(self, text="Go to more pull data [to be implemented]", command=lambda: controller.show_frame(PullDataF))
        button3.pack()

        button4 = Button(self, text="Compare this data to the averages [to be implemented]", command=lambda: controller.show_frame(AverageDataF))
        button4.pack()

    def update(self):
        global firstColumn, secondColumn, mean1, mean2, upperPercentile, lowerPercentile, paceDistribution, pullDistribution, paceProcessed, pullProcessed
        global colorDict, paceBorders, pullBorders, paceArea, pullArea
        self.text1.delete('1.0', END)


        paceString = "The average pace of the dog is: %s\n\n" % mean1
        pullString = "The average pull of the dog is: %s\n\n" % mean2
        self.text1.insert(END, paceString)
        self.text1.insert(END, pullString)

        self.text1.tag_add("paceColor", "1.32", "1.36")
        self.text1.tag_add("pullColor", "3.32", "3.36")

        paceColor = colorDict[paceArea]
        pullColor = colorDict[pullArea]

        self.text1.tag_config("paceColor", background=paceColor, foreground="blue")
        self.text1.tag_config("pullColor", background=pullColor, foreground="blue")


class PaceDataF(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Pace Data", font=DEFAULT_FONT)
        label.pack(pady=10,padx=10)

        button1 = Button(self, text="Back to Basic Data", command=lambda: controller.show_frame(BasicDataF))
        button1.pack(pady=20,padx=20)

        global dataIn
        self.f = Figure(figsize =(2,2))
        # self.f.suptitle("Pace Data Display")
        self.a = self.f.add_subplot(1,2,1)
        self.b = self.f.add_subplot(1,2,2)
        self.canvas = FigureCanvasTkAgg(self.f, master=self)

        # self.text1 = Text(self, height=32, width=32)
        # self.text1.config(width=50, height=5)
        # self.text1.pack_propagate(0)
        # self.text1.pack()


    def update(self):
        global firstColumn, secondColumn, mean1, mean2, upperPercentile, lowerPercentile, paceDistribution, pullDistribution, paceProcessed, pullProcessed
        global colorDict, paceBorders, pullBorders, paceArea, pullArea, paceBins, pullBins

        self.a.clear()
        self.b.clear()
        print(dataIn)
        first = list(dataIn[firstColumn])
        second = list(dataIn[secondColumn])
        print(first)
        print(second)
        self.a.plot(first)
        self.a.set_title('Pace over Time')


        self.b.hist(second, bins=pullBins)
        self.b.patches[0].set_color('r')
        self.b.patches[1].set_color('b')
        self.b.patches[2].set_color('g')
        self.b.patches[3].set_color('b')
        self.b.patches[4].set_color('r')
        self.b.set_title('Histogram of Pace Distribution')

        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=0)

class PullDataF(Frame):
    def __init__():
        pass

def main():
    # matplotlib.pyplot.subplots_adjust()
    app = containerClass()
    app.mainloop()


if __name__ == '__main__':
    main()

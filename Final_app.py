#!/usr/bin/env python3
'''
An application created for the Seeing Eye to aid in guide dog pairings

Made for Technology, Accessibility, & Design Spring 2019
Team Members: Nathan Lepore, Nicole Scheubert, Nicholas Sherman
'''

#Import Statements
from tkinter import Tk, BOTH, Label, TOP, YES, Text, END, Button, font, DISABLED, PhotoImage
from tkinter.ttk import Frame, Style
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
import pandas as pd
import matplotlib
matplotlib.use("TkAgg") #it's the backend of matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import numpy as np
import os
from matplotlib.patches import Rectangle
#Set the directory path of where we are now. The + "/../.." is to be implemented for executables.
dir_path = os.path.dirname(os.path.realpath(__file__))  + "/../.."


#Constant Declarations
TITLE_FONT = ("Verdana", 30)
TEXT_FONT = ("Verdana", 18)
DEFAULT_FONT_BUTTON = 0 #Having issues with working correctly
HEIGHT = 800    #Of the application's interface
WIDTH = 700     #Of the application's interface
BUTTON_HEIGHT = 1
BUTTON_WIDTH = 30


#Global Variable Starts

hspacee = 0.35  #Dictates the amount of space between subplots.

dataIn = 0      #Stores the read data in
fileloc = 0     #Saves the location of the file that is read.

paceDistribution = [0, 0, 0, 0, 0]  #Saves distribution of pace in the different buckets given by the Seeing Eye
pullDistribution = [0, 0, 0, 0, 0]  #Saves distribution of pull in the different buckets given by the Seeing Eye

paceProcessed = 0   #List of the pace data after being processed
paceTimes = 0       #Corresponding list of pace times
pullProcessed = 0   #List of the pull data after being processed
pullTimes = 0       #List of the pull times

#Name of columns of relevent data.
firstColumn = "Pace"
secondColumn = "Pull"
thirdColumn = "Time"

#Sets the limit of data that is eliminated from the sample set.
upperPercentile = 95
lowerPercentile = 5

meanPace = -1  #Saves the mean pace of the dog after data processing
meanPull = -1  #Saves the mean pull of the dog after processing

#Set up different color combinatiosn for the color dictionary used to decide the color of highlighting in the data information page.
RED_COLORING = "#FF3300"
GREEN_COLORING = "#7CFC00"
YELLOW_COLORING = "yellow"
colorDict = {0:RED_COLORING, 1:YELLOW_COLORING, 2:GREEN_COLORING, 3:YELLOW_COLORING, 4:RED_COLORING}
descriptionDict = {0:"significantly below average", 1:"below average", 2:"average", 3:"above average", 4:"significantly above average"}

#Note the boundaries
paceBorders = [2.0, 2.45, 3.25, 3.95]
pullBorders = [2.5, 5.0, 7.5, 10]

#Says where in the buckets the mean falls.
paceArea = -1
pullArea = -1


#TODO (outside of scope of project):
'''
1) Less whitespace above the Pace/pull over time graphs
2) More space on pages between things (padding) to balance the empty space
3) Text descriptions of graphs

BACKBURNER:
1) Plot showing walk; color code to show how fast? Also color code for pull?
2) Google Maps API for above?
'''

def DataCalculations():
    #Function that completes all application-backend calculations on the imported data.
    global firstColumn, secondColumn, meanPace, meanPull, upperPercentile, lowerPercentile, paceDistribution, pullDistribution, paceProcessed, pullProcessed
    global paceBorders, pullBorders, paceArea, pullArea, thirdColumn, paceTimes, pullTimes

    #Extract the raw data from the imported data
    rawPace = np.array(dataIn[firstColumn])
    rawPull = np.array(dataIn[secondColumn])
    rawTimes = np.array(dataIn[thirdColumn])
    y = rawTimes[0]
    for x in range(0, len(rawTimes)):
        rawTimes[x] = (rawTimes[x] - y)/1000 #Account for ms -> s

    # for x in range(0, len(rawPull)):
    #     rawPull[x] = (rawPull[x])/10 #Eyeballed to convert sensor data to ~pounds. Now done in Arduino.

    #Get the bounds on the data based on the percentiles
    highBound1 = np.percentile(rawPace, upperPercentile)
    lowBound1 = np.percentile(rawPace, lowerPercentile)
    highBound2 = np.percentile(rawPull, upperPercentile)
    lowBound2 = np.percentile(rawPull, lowerPercentile)

    #Holder lists
    valid_nums1 = []
    valid_times1 = []
    valid_nums2 = []
    valid_times2 = []

    #Add the data to the valid_nums array. To be changed to have a matching time array once implemented.
    for x in range(0, len(rawPace)):
        if rawPace[x] <= highBound1 and rawPace[x] >= lowBound1:
            valid_nums1.append(rawPace[x])
            valid_times1.append(rawTimes[x])


    for x in range(0, len(rawPull)):
        if rawPull[x]<= highBound2 and rawPull[x] >= lowBound2:
            valid_nums2.append(rawPull[x])
            valid_times2.append(rawTimes[x])

    #Cast what ended up being a np array to a list and set it to the global information.
    paceProcessed = list(valid_nums1)
    pullProcessed = list(valid_nums2)
    paceTimes = valid_times1
    pullTimes = valid_times2
    # print(paceTimes)
    # print(pullTimes)

    #Sort the data for more processing.
    valid_nums1.sort()
    valid_nums2.sort()

    valid_nums1 = np.array(valid_nums1)
    valid_nums2 = np.array(valid_nums2)

    #Means -- let it be of middle 90% of data?
    meanPace = np.mean(valid_nums1)
    meanPull = np.mean(valid_nums2)

    #Figure out in what bracket the average pace/pull is (what "Area" it's in)
    if(meanPace < paceBorders[0]):
        paceArea = 0;
    elif(meanPace < paceBorders[1]):
        paceArea = 1;
    elif(meanPace < paceBorders[2]):
        paceArea = 2;
    elif(meanPace < paceBorders[3]):
        paceArea = 3;
    else:
        paceArea = 4;

    if(meanPull < pullBorders[0]):
        pullArea = 0;
    elif(meanPull < pullBorders[1]):
        pullArea = 1;
    elif(meanPull < pullBorders[2]):
        pullArea = 2;
    elif(meanPull < pullBorders[3]):
        pullArea = 3;
    else:
        pullArea = 4;

    #Distributions -- hardcoded based off of the sheet provided to us by our community partner
    paceDistribution[0] =  len(valid_nums1[ np.where( valid_nums1.all() < paceBorders[0] ) ])
    paceDistribution[1] =  len(valid_nums1[ np.where( valid_nums1.all() < paceBorders[1] and valid_nums1.all() >= paceBorders[0] ) ])
    paceDistribution[2] =  len(valid_nums1[ np.where( valid_nums1.all() < paceBorders[2] and valid_nums1.all() >= paceBorders[1] ) ])
    paceDistribution[3] =  len(valid_nums1[ np.where( valid_nums1.all() < paceBorders[3] and valid_nums1.all() >= paceBorders[2] ) ])
    paceDistribution[4] =  len(valid_nums1[ np.where( valid_nums1.all() >= paceBorders[3] ) ])

    # print(pullDistribution[0])
    # print(pullBorders[0])
    # print(valid_nums2)
    # print(highBound2)
    # print(lowBound2)
    pullDistribution[0] =  len(valid_nums2[ np.where( valid_nums2.all() < pullBorders[0] ) ])
    pullDistribution[1] =  len(valid_nums2[ np.where( valid_nums2.all() < pullBorders[1] and valid_nums2.all() >= pullBorders[0] ) ])
    pullDistribution[2] =  len(valid_nums2[ np.where( valid_nums2.all() < pullBorders[2] and valid_nums2.all() >= pullBorders[1] ) ])
    pullDistribution[3] =  len(valid_nums2[ np.where( valid_nums2.all() < pullBorders[3] and valid_nums2.all() >= pullBorders[2] ) ])
    pullDistribution[4] =  len(valid_nums2[ np.where( valid_nums2.all() >= pullBorders[3] ) ])

class containerClass(Tk):
    #Container class that extends the base Tk container.

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, None, None)   #It's parent class's init is necessary.

        #Start a container
        container = Frame(self)
        # container.configure(background="white")

        #Try to set the default font button (issues regarding this still)
        DEFAULT_FONT_BUTTON = font.Font(family='Verdana', size=130, weight='bold')

        #Set up the container properties
        container.pack(sid="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        geometryString = str(WIDTH) + "x" + str(HEIGHT) #Convert the global variables to a string in the format geometry is looking for.
        self.geometry(geometryString)

        #Set up a dictionary of frames and then popula
        self.frames = {}
        for F in (DataImportF, BasicDataF, PaceDataF, PullDataF):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame

        #Show the first frame
        self.show_frame(DataImportF)

    def requestInfo(self):
        #Prompts the user to choose the csv containing the data of the walk to be analyzed.
        global dataIn, fileloc
        filename = askopenfilename(initialdir = dir_path,title = "Select file") # show an "Open" dialog box and return the path to the selected file
        fileloc = filename
        dataIn = pd.read_csv(fileloc)
        DataCalculations() #Perform the data calculations elsewhere.
        self.show_frame(BasicDataF) #Show the frame with the basic data.

    def show_frame(self, cont):
        #Shows the desired frame, calls the frame's corresponding update function (which could just pass), then raise the frame to the top of the stack.
        frame = self.frames[cont]
        frame.update()
        frame.tkraise()


class DataImportF(Frame):
    #Class that holds the first frame, where the user can import their data.

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)    #Call tkinter's class init.
        # self.configure(background="white")

        #Set up the top label of the page.
        label = Label(self, text="Data Import Page", font=TITLE_FONT)
        label.pack(pady=10,padx=10)

        # img = ImageTk.PhotoImage(Image.open("seeingeye.jpg"))
        loaded = Image.open("seeingeye.jpg")
        loaded = loaded.resize((250, 250), Image.ANTIALIAS)
        rendered = ImageTk.PhotoImage(loaded)
        img = Label(self, image=rendered)
        img.image = rendered
        img.pack()


        #Set up the buttons that allow the user to import the data they have. Buttons 2/3 we did not have time to implement.
        button1 = Button(self, text="Import Pace & Pull Data", bg="white", command=lambda: controller.requestInfo())
        button1.config(width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=DEFAULT_FONT_BUTTON) #, width = BUTTON_WIDTH)
        button1.pack()

        # button2 = Button(self, text="Imported Only Pace Data (coming soon)")#, command=lambda: controller.show_frame(PageOne))
        # button2.pack()
        #
        # button3 = Button(self, text="Imported Only Pull Data (coming soon)")#, command=lambda: controller.show_frame(PageOne))
        # button3.pack()

    def update(self):
        #Unneeded for this Frame.
        pass

class BasicDataF(Frame):
    #Frame containing the basic data summarized for readers.
    def __init__(self, parent, controller):
        Frame.__init__(self, parent) #Call parent init.

        #Set up the label saying what page it is.
        label = Label(self, text="Basic Data Information", font=TITLE_FONT)
        label.pack(pady=10,padx=10)

        #Back button
        button1 = Button(self, text="Back to Import Page", bg="white", command=lambda: controller.show_frame(DataImportF))
        button1.config(width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=DEFAULT_FONT_BUTTON) #, width = BUTTON_WIDTH)
        button1.pack()

        #Set up the text class that holds the importan user data
        self.text1 = Text(self, height=32, width=32)
        self.text1.config(width=46, height=10, font=TEXT_FONT)
        self.text1.pack_propagate(0)
        self.text1.pack()

        #Set up buttons going to more data pages.
        button2 = Button(self, text="Go to more pace data", bg="white", command=lambda: controller.show_frame(PaceDataF))
        button2.config(width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=DEFAULT_FONT_BUTTON)
        button2.pack()

        button3 = Button(self, text="Go to more pull data", bg="white", command=lambda: controller.show_frame(PullDataF))
        button3.config(width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=DEFAULT_FONT_BUTTON)
        button3.pack()

        # button4 = Button(self, text="Compare this data to the averages [to be implemented]", command=lambda: controller.show_frame(AverageDataF))
        # button4.config(width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=DEFAULT_FONT_BUTTON)
        # button4.pack()

    def update(self):
        #Update the displayed data based on input information.
        global firstColumn, secondColumn, meanPace, meanPull, upperPercentile, lowerPercentile, paceDistribution, pullDistribution, paceProcessed, pullProcessed
        global colorDict, paceBorders, pullBorders, paceArea, pullArea, descriptionDict, thirdColumn, paceTimes, pullTimes

        self.text1.config(state="normal")

        self.text1.delete('1.0', END)   #Erase old data from textbox

        #Input the basic strings
        paceString = "The average pace of the dog in mph is: %2.2f\n" % meanPace
        pullString = "The average pull of the dog in lbs is: %2.2f\n\n" % meanPull
        self.text1.insert(END, paceString)
        self.text1.insert(END, pullString)

        #Format the text as desired.
        self.text1.tag_add("paceColor", "1.39", "1.49")
        self.text1.tag_add("pullColor", "2.39", "2.49")
        self.text1.tag_add("Justification", "0.0", "10.100")
        paceColor = colorDict[paceArea]
        pullColor = colorDict[pullArea]
        self.text1.tag_config("paceColor", background=paceColor)
        self.text1.tag_config("pullColor", background=pullColor)
        self.text1.tag_config("Justification", justify="center")

        paceDescription = "The pace of this dog is %s.\n" % descriptionDict[paceArea]
        pullDescription = "The pull of this dog is %s.\n\n" % descriptionDict[pullArea]
        self.text1.insert(END, paceDescription)
        self.text1.insert(END, pullDescription)


        infoString = "Color Coding:\n Far From Average Value\n Near Average Value\n Average Value"
        self.text1.insert(END, infoString)
        self.text1.tag_add("colorCode1", "8.1", "8.23")
        self.text1.tag_add("colorCode2", "9.1", "9.23")
        self.text1.tag_add("colorCode3", "10.1", "10.23")
        self.text1.tag_config("colorCode1", background=colorDict[0])
        self.text1.tag_config("colorCode2", background=colorDict[1])
        self.text1.tag_config("colorCode3", background=colorDict[2])

        self.text1.config(state=DISABLED)

class PaceDataF(Frame):
    #Frame containing the pace data frame
    def __init__(self, parent, controller):
        #Basic frame setup
        global hspacee
        Frame.__init__(self, parent)

        #Page defining label
        label = Label(self, text="Pace Data", font=TITLE_FONT)
        label.pack(pady=10,padx=10)

        #Back button
        button1 = Button(self, text="Back to Basic Data", bg="white", command=lambda: controller.show_frame(BasicDataF))
        button1.config(width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=DEFAULT_FONT_BUTTON)
        button1.pack(pady=20,padx=20)

        #Set up the figure with subplots
        self.f = Figure(figsize =(4,8))
        self.f.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=hspacee)
        # self.f.suptitle("Pace Data Display")
        self.a = self.f.add_subplot(2,1,1)
        self.b = self.f.add_subplot(2,1,2)
        self.canvas = FigureCanvasTkAgg(self.f, master=self)

    def update(self):
        #Calls the update graph method using the "Pace" distinction
        updateGraph(self, "Pace")

class PullDataF(Frame):
    #Frame containing the Pull Data Information

    def __init__(self, parent, controller):
        #Basic frame setup
        global hspacee
        Frame.__init__(self, parent)

        #Page defining label
        label = Label(self, text="Pull Data", font=TITLE_FONT)
        label.pack(pady=10,padx=10)

        #Back button
        button1 = Button(self, text="Back to Basic Data", bg="white", command=lambda: controller.show_frame(BasicDataF))
        button1.config(width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=DEFAULT_FONT_BUTTON)
        button1.pack(pady=20,padx=20)

        #Set up the figure with subplots
        self.f = Figure(figsize =(4,8))
        self.f.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=hspacee)
        # self.f.suptitle("Pace Data Display")
        self.a = self.f.add_subplot(2,1,1)
        self.b = self.f.add_subplot(2,1,2)
        self.canvas = FigureCanvasTkAgg(self.f, master=self)

    def update(self):
        #Calls the update graph method using the "Pace" distinction
        updateGraph(self, "Pull")

def updateGraph(FrameIn, type):
    #Updates the graphs on the "update" page. Allows for input of "Pace" or "Pull" with the frame being changed to update the correct graph.
    global firstColumn, secondColumn, meanPace, meanPull, upperPercentile, lowerPercentile, paceDistribution, pullDistribution, paceProcessed, pullProcessed
    global colorDict, paceBorders, pullBorders, paceArea, pullArea, thirdColumn, paceTimes, pullTimes

    #Clear old data.
    FrameIn.a.clear()
    FrameIn.b.clear()

    #Set the data for pace or pull frame
    if(type == "Pace"):
        data = list(paceProcessed)
        borders = paceBorders
        axisLabel = "Speed (mph)"
        times = paceTimes
    else:
        data = list(pullProcessed)
        borders = pullBorders
        axisLabel = "Force (lbs)"
        times = pullTimes

    #Set up scatterplot
    title1 = type + " Over Time"
    title2 = "Histogram of " + type + " Distribution"
    # FrameIn.a.scatter(range(0, len(data)), data) #TODO:Change to over time
    FrameIn.a.plot(times, data, linestyle='-', marker='o')

    FrameIn.a.set_title(title1)
    FrameIn.a.set(xlabel="Time (s)", ylabel=axisLabel)

    #Set up and then color histogram
    FrameIn.b.hist(data)
    for i, rectangle in enumerate(FrameIn.b.patches):  # iterate over every bar
        tmp = abs(rectangle.get_x() + rectangle.get_width() )
        if tmp < borders[0]:  # we are searching for the bar with x cordinate
            FrameIn.b.patches[i].set_color('r')
        elif tmp < borders[1]:
            FrameIn.b.patches[i].set_color('b')
        elif tmp < borders[2]:
            FrameIn.b.patches[i].set_color('g')
        elif tmp < borders[3]:
            FrameIn.b.patches[i].set_color('b')
        else:
            FrameIn.b.patches[i].set_color('r')
    FrameIn.b.set_title(title2)
    FrameIn.b.set(xlabel=axisLabel, ylabel="Number of Measurements")
    handles = [Rectangle((0,0),1,1,color=c,ec="k") for c in ['r','b','g']]
    labels = ["Far from Average","Close to Average", "Average"]
    FrameIn.b.legend(handles, labels)
    FrameIn.canvas.draw()
    FrameIn.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=0)

def main():
    #Instantiate the app then run its mainloop (function that tkinter runs)
    app = containerClass()
    app.mainloop()


#Set up the main function
if __name__ == '__main__':
    main()

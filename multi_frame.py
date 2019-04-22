from tkinter import Tk, BOTH, Label, TOP, YES
from tkinter.ttk import Frame, Button, Style
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename

LARGE_FONT = ("Verdana", 12)

class tempTk(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)

        container.pack(sid="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame


        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = Button(self, text="Visit Page", command=lambda: controller.show_frame(PageOne))
        button1.pack()

        button2 = Button(self, text="Visit Page", command=lambda: controller.show_frame(PageOne))
        button2.pack()

        button3 = Button(self, text="Visit Page", command=lambda: controller.show_frame(PageOne))
        button3.pack()

class PageOne(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Page 1", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()


app = tempTk()
app.mainloop()

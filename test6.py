from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
dir_path = os.path.dirname(os.path.realpath(__file__)) + "/.."

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(initialdir = dir_path,title = "Select file") # show an "Open" dialog box and return the path to the selected file
print(filename)

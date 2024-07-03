from tkinter import *
from tkinter import ttk

class App(Frame):
    def __init__(self, master):
        super().__init__(master)
        master.geometry("960x540")
        master.resizable(False,False)

        #Menubar Setup
        self.mainMenubar = Menu(master)
        self.fileMenu = Menu(self.mainMenubar, tearoff=0)
        self.helpMenu = Menu(self.mainMenubar, tearoff=0)
        self.viewMenu = Menu(self.mainMenubar, tearoff=0)
        self.configMenu = Menu(self.mainMenubar, tearoff=0)
        self.mainMenubar.add_cascade(label="File", menu=self.fileMenu)
        self.mainMenubar.add_cascade(label="View", menu=self.viewMenu)
        self.mainMenubar.add_cascade(label="Configuration", menu=self.configMenu)
        self.mainMenubar.add_cascade(label="Help", menu=self.helpMenu)
        
        master.config(menu=self.mainMenubar)

        #Display Setup
        self.mainDisplay = Frame(master, relief="sunken", borderwidth= 1, width=500, height=538)
        self.mainDisplay.grid_propagate(False)
        self.mainDisplay.grid(row=0, rowspan=2, column=0, columnspan=1)
        
        self.mainSpacer = Frame(master, width=154)
        self.mainSpacer.grid(row=0, rowspan=1, column=1, columnspan=1)

        self.mainControl = Frame(master, relief="raised", borderwidth=1, width=300, height=538)
        self.mainControl.grid_propagate(False)
        self.mainControl.grid(row=0, rowspan=1, column=2, columnspan=1)
         
        self.test2 = Entry(self.mainDisplay)
        self.test2.grid(row=0, column=0)
        self.test = Entry(self.mainControl)
        self.test.grid(row=0, column=0)


root = Tk()    
myapp = App(root)
myapp.mainloop()
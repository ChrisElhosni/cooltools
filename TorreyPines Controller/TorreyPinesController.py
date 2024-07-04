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
        self.mainDisplayLabel = Label(self.mainDisplay, text="Current State and Information")
        self.mainDisplayLabel.grid(row=0, column=0)
        
        self.mainSpacer = Frame(master, width=154)
        self.mainSpacer.grid(row=0, rowspan=1, column=1, columnspan=1)

        self.mainControl = Frame(master, relief="raised", borderwidth=1, width=300, height=538)
        self.mainControl.grid_propagate(False)
        self.mainControl.grid(row=0, rowspan=1, column=2, columnspan=1)
        self.mainControlLabel = Label(self.mainControl, text="Controls")
        self.mainControlLabel.grid(row=0, column=0, columnspan=3)

        #Controls
        #Temperature Control
        self.tempControlLabel = Label(self.mainControl, text="Temperature \u2103")
        self.tempControlLabel.grid(row=1, column=0)

        def tempValidation(value):
            if str.isdigit(value) and 100>=int(value)>=0:
                return True
            elif str(value) == "":
                return True
            else:
                return False
            
        validationCommand = self.register(tempValidation)

        self.tempControl = Entry(self.mainControl, width=5)
        self.tempControl.insert(0, "25")
        self.tempControl.config(validate="key", validatecommand=(validationCommand, "%P"))
        self.tempControl.grid(row=1, column=1)

        self.tempControlButton = Button(self.mainControl, text="Set Temp")
        self.tempControlButton.grid(row=1, column=2)
        
        #Idle Control
        self.idleControl = Button(self.mainControl, text="Idle", width=35)
        self.idleControl.grid(row=2, column=0, columnspan=3)




root = Tk()    
myapp = App(root)
myapp.mainloop()
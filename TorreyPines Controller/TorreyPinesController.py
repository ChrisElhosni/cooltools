#Check if any of this is really needed, other than tkinter * and serial
from tkinter import *
from tkinter import messagebox
from time import sleep
import random
import serial
import serial.tools
import serial.tools.list_ports
import re

#TO COMPILE, I run 'python -m PyInstaller --noconsole --onefile "C:\Users\chris\Desktop\ChrisElhosni\coolTools\TorreyPines Controller\TorreyPinesController.py"'

class App(Frame):
    def __init__(self, master):
        super().__init__(master)
        master.geometry("960x540")
        master.resizable(False,False)
        master.title("TorreyPines Control v0.1")
        self.itemList = []
        units = 11
        self.unitList = []
        self.checkValList = []
        self.serialConnections = []

        #Menubar Setup
        self.mainMenubar = Menu(master)
        self.fileMenu = Menu(self.mainMenubar, tearoff=0)
        self.helpMenu = Menu(self.mainMenubar, tearoff=0)
        self.viewMenu = Menu(self.mainMenubar, tearoff=0)
        self.configMenu = Menu(self.mainMenubar, tearoff=0)
        self.configMenu.add_command(label="Detect and Connect")
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
                messagebox.showinfo(title="Exceeded Temperature Limits", message="The minimum set temperature is 0\u2103 and the maximum set temperature is 100\u2103")
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

        #Test Button
        self.testButton = Button(self.mainControl, text="Test", width = 35)
        self.testButton.grid(row=4, column=0, columnspan=3)

        def checkboxControlTrue():
            for eachCheckbox in self.itemList:
                    eachCheckbox[3].select()

        def checkboxControlFalse():
            for eachCheckbox in self.itemList:
                    eachCheckbox[3].deselect()
            
        #Select All
        self.checkAll = Button(self.mainControl, text="Select All", width = 15, command=checkboxControlTrue)
        self.checkAll.grid(row=3, column= 0)

        #Deselect All
        self.uncheckAll = Button(self.mainControl, text="Deselect All", width = 15, command=checkboxControlFalse)
        self.uncheckAll.grid(row=3, column= 2)

        #Display
        self.unitBox = Canvas(self.mainDisplay, height=300, width=490)
        self.unitBox.pack_propagate(False)
        self.unitBox.grid(row=1, column=0)
        
        #Captions
        self.Captions = Frame(self.unitBox)
        self.Captions.pack(side="top")

        self.nameCaption = Label(self.Captions, text="Unit Name", width=20, anchor="w")
        self.nameCaption.grid(row=0, column=0)

        self.currentTempCaption = Label(self.Captions, text="Current Temperature", width=25)
        self.currentTempCaption.grid(row=0, column=1)

        self.setTempCaption = Label(self.Captions, text="Set Temperature", width = 20)
        self.setTempCaption.grid(row=0, column=2)

        for unit in range(units):
            self.itemList.append([])
            self.unitList.append(Frame(self.unitBox))
            self.unitList[unit].pack(side="top")

            #Label is 0 index
            self.itemList[unit].append(Label(self.unitList[unit], text=f"TorreyPines Unit {unit + 1}", width=20, anchor="w"))
            self.itemList[unit][0].grid(row=0, column=0)

            #Current Temp is 1 index
            self.itemList[unit].append(Entry(self.unitList[unit], width = 25))
            self.itemList[unit][1].insert(0, "UNKNOWN")
            self.itemList[unit][1].config(state="readonly")
            self.itemList[unit][1].grid(row=0, column=1)

            #Set Temp is 2 index
            self.itemList[unit].append(Entry(self.unitList[unit], width = 20))
            self.itemList[unit][2].insert(0, "NOT SET")
            self.itemList[unit][2].config(state="readonly")
            self.itemList[unit][2].grid(row=0, column=2)

            #Checkbox is 3 index
            self.checkValList.append(IntVar(master,0))
            self.itemList[unit].append(Checkbutton(self.unitList[unit], variable=self.checkValList[unit]))
            self.itemList[unit][3].grid(row=0, column=3)
            self.itemList[unit][3].config

        #     # keeping this for POC - we can programatically generate widgets that we can reference through a unit[].control[] method
        #     # for item in range(5):
        #     #     self.itemList.append([])    
        #     #     self.itemList[unit].append(Label(self.unitList[unit], text=f"Item {item + unit*5 +1}"))
        #     #     self.itemList[unit][item].grid(row=0, column=item, sticky="W")
        
        #eventually, we'll have this set up at the top, and itll determine how many units to build for front end stuff, so we dont run into "index out of range" errors when we try and call our commands
        #detect units uses the serial tools listports function to grab a list of listPortInfo objects and translate them into an list of serial connections ordered by port#
        def detectUnits() -> list:
            self.serialConnections.clear()
            messageOut = ""

            comPortList = serial.tools.list_ports.comports()

            #Detect units, then validate device name
            if len(comPortList) == 0:
                messagebox.showinfo(title="Detect Units", message="No COM Ports detected")
                return
            else:
                for comPortUnit in comPortList:
                    foundPort = re.search(r"\bCOM\d+", comPortUnit.device)
                    if foundPort != None:
                        self.serialConnections.append(serial.Serial(port=foundPort.group(), baudrate= 9600, parity= "N", stopbits= 1, timeout=0.5))
            
            #sort connections
            self.serialConnections.sort(key= lambda a : re.search(r"(?<=COM)\d+", a).group())

            #validate connection
            for connection in self.serialConnections:
                #send command for get SN of TP unit
                connection.write(b"V\r")
                response = connection.readline().decode("UTF-8")

                #If response is not a string of 8 numbers (a SN), close the connection and remove it from the serialConnections list
                if re.search(r"\d{8}", response) != None:
                    messageOut += f"SN: {response} is connected to {connection.port}\n"
                else:
                    connection.close()
                    self.serialConnections.remove(connection)
            messagebox.showinfo(title="Detect Units", message=messageOut)
        self.configMenu.entryconfigure(0, command=detectUnits)
        
        def setTemp():
            temperature = self.tempControl.get()
            for unit in range(units):
                if self.checkValList[unit].get() == 1:
                    #write set temp to unit
                    #turn off for demo
                    #self.serialConnections[unit].write(bytes(f"n{temperature}\r"))
                    
                    #ask for set temp for unit, should return a number
                    #turn off for demo
                    #self.serialConnections[unit].write(b"s\r")

                    self.itemList[unit][2].config(state="normal")
                    self.itemList[unit][2].delete(0, END)
                    #turn off for demo
                    #self.itemList[unit][2].insert(0, f"{self.serialConnections[unit].readline().decode("UTF-8")} \u2103")
                    self.itemList[unit][2].insert(0, f"{temperature} \u2103")
                    self.itemList[unit][2].config(state="readonly")
        self.tempControlButton.config(command=setTemp)

        def idle():
            for unit in range(units):
                if self.checkValList[unit].get() == 1:
                    #write idle to unit
                    #turn off for demo
                    #self.serialConnections[unit].write(bytes(f"i\r"))

                    #ask for set temp for unit, should return off
                    #turn off for demo
                    #self.serialConnections[unit].write(b"s\r")

                    self.itemList[unit][2].config(state="normal")
                    self.itemList[unit][2].delete(0, END)
                    #turn off for demo
                    #self.itemList[unit][2].insert(0, f"{self.serialConnections[unit].readline().decode("UTF-8")}")
                    self.itemList[unit][2].insert(0, "IDLE")
                    self.itemList[unit][2].config(state="readonly")
        self.idleControl.config(command=idle)

        #we make getTempSingle only get temp for a single unit so we can pipe each call as a different background tasks that get added to the event queue (using updateCurrentTemp) once every 3-5 seconds
        def getTempSingle(unit):
            #turn off for demo
            # self.serialConnections[unit].write(bytes(f"p\r"))

            #this only changes UI
            self.itemList[unit][1].config(state="normal")
            self.itemList[unit][1].delete(0, END)
            #turn off for demo
            #self.itemList[unit][1].insert(0, f"{self.serialConnections[unit].readline().decode("UTF-8")} \u2103")
            #Random number option
            self.itemList[unit][1].insert(0, f"{random.uniform(0, 100):.1f} \u2103")
            self.itemList[unit][1].config(state="readonly")

        def updateCurrentTemp():
            for unit in range(units):    
                master.after_idle(getTempSingle, unit)
            master.after(5000, updateCurrentTemp)
        #(TO DO) Reenable and Move the master.after call to after connections are made
        master.after(1000, updateCurrentTemp)
        
        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                #(TO DO) Re enable the close alert
                messagebox.showinfo(title="Shutdown", message="All TorreyPines Units will be set to Idle")
                for eachCheckbox in self.itemList:
                    eachCheckbox[3].select()
                #(TO DO) Re enable idle
                #idle()
                for connection in self.serialConnections:
                    connection.close
                master.destroy()
        master.protocol("WM_DELETE_WINDOW", on_closing)




        #Test Button Tie
        #self.testButton.config(command=detectUnits)

# #BACKEND TEST WORKS
#ser = serial.Serial(port="COM11", baudrate = 9600, parity= "N", stopbits= 1)
# ser.write(b"v\r")
# sleep(50)

# data=ser.readline()
# print(data.decode('UTF-8'))
# ser.close()

# #list comports
# for each in serial.tools.list_ports.comports():
#      print(each)

            

root = Tk()    
myapp = App(root)
myapp.mainloop()
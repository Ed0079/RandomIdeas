import sqlite3
import _random
import random
import tkinter
from tkinter import *
import customtkinter
from customtkinter import *

con =  sqlite3.connect("MachineDB.db")
cur = con.cursor()
window = CTk()
window.title("Random Idea")
window.eval('tk::PlaceWindow . center')
window.geometry("375x150")

# The add/remove window
class ExtraWindow(customtkinter.CTkToplevel):
    # Choice both sets a variable and passes to the main body/code of the extra window
    def choice(self, i):
        self.num = i
        return self.__int__()

    def __int__(self):
        # Setting the window's layout depending on the choice(remove or add)
        window.eval(f'tk::PlaceWindow {str(self)} center')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)

        if self.num == 1:
            self.title("Add")
            self.geometry("400x75")
        elif self.num == 2:
            self.title("Remove")
            self.geometry("300x75")

        self.layout()

    def layout(self):
        self.DropBoxLabel01 = customtkinter.StringVar()
        self.Buttons = CTkButton(self, text=" ", font=('consolas', 19))
        if self.num == 1:
            self.DropBoxLabel01.set("Slot01")
            self.DropBox = CTkOptionMenu(self, variable=self.DropBoxLabel01, values=["Slot01", "Slot02", "Slot03"], width=6)
            self.DropBox.configure(font=('consolas', 19))
            self.Input = CTkEntry(self, font=('consolas', 15), width=200)
            self.Buttons.configure(text="+", command=lambda: self.ID(1), width=35)

        elif self.num == 2:

            self.DropBoxLabel02 = customtkinter.StringVar()
            self.DropBoxLabel02.set(" "*10)
            self.DropBoxLabel01.set(" ")
            self.DropBoxLabel01.trace('w', self.Update)
            self.DropBox = CTkOptionMenu(self, variable=self.DropBoxLabel01, values=["Slot01", "Slot02", "Slot03"])
            self.DropBox.configure(font=('consolas', 19), width=100)
            self.Input = CTkOptionMenu(self, variable=self.DropBoxLabel02, values=[""])
            self.Input.configure(font=('consolas', 19), width=100)
            self.Buttons.configure(text="-", command=lambda: self.ID(2), width=35)

        self.DropBox.configure(font=('consolas', 19))
        self.DropBox.grid(row=1, column=0)
        self.Input.grid(row=1, column=1)
        self.Buttons.grid(row=1, column=2)

    # The function that inserts/deletes data to the database
    def ID(self, i):

        if i == 1:
            w = ""

            for row in cur.execute("SELECT Number FROM RandomSlots where Slot ='" + str(self.DropBoxLabel01.get()) + "'"):
                w = int(row[0]) + 1
            cur.execute("INSERT INTO RandomSlots VALUES ('"+str(self.DropBoxLabel01.get())+"','"+str(w)+"','"+str(self.Input.get())+"')")

        elif i == 2:
            cur.execute("DELETE FROM RandomSlots WHERE Name = '"+str(self.DropBoxLabel02.get())+"' and Slot ='"+str(self.DropBoxLabel01.get())+"'")

        con.commit()
        self.destroy()
    # This function is exclusive for 'remove' and what it does is that when the user
    # selects from the option menu (DropBox) it will fill the second option menu (input)
    # with all the data that is associated with the selected option in the first menu.
    # Ej. Slot01 has Hi, Hello, Holla , ect. then Input=[Hi, Hello, Holla,ect.] and
    # when a new option is selected it will erase the previous data and start a new.
    def Update(self,*args):
        self.DropBoxLabel02.set(" "*10)
        self.Input.configure(values=" ")
        self.new_values = []

        for row in cur.execute("SELECT Name FROM RandomSlots where Slot ='" + str(self.DropBoxLabel01.get()) + "' "):
            self.new_values.append(row[0])

        self.Input.configure(values=self.new_values)


def randomint(s):

    r = ""
    for row in cur.execute("SELECT Number FROM RandomSlots where Slot ='"+str(s)+"' "):
        n = row[0]
    if n != 0:
        r = random.randint(1, int(n))

    return str(r)

def get01():
   x = ""

   for row in cur.execute("SELECT Name FROM RandomSlots where Slot ='Slot01' and Number =" + randomint("Slot01")):
    x = row[0]

   return str(x)

def get02():

   y = ""

   for row in cur.execute("SELECT Name FROM RandomSlots where Slot ='Slot02' and Number =" + randomint("Slot02")):
    y = row[0]

   return str(y)

def get03():

   z = ""
   for row in cur.execute("SELECT Name FROM RandomSlots where Slot ='Slot03' and Number =" + randomint("Slot03")):
    z = row[0]

   return str(z)

def spin():

    label1.configure(text=get01())

    label2.configure(text=get02())

    label3.configure(text=get03())

# The layout for the first window
set_appearance_mode("Dark")
label1 = CTkLabel(window, text="", font=('consolas', 25))
label2 = CTkLabel(window, text="", font=('consolas', 25))
label3 = CTkLabel(window, text="", font=('consolas', 25))
add = CTkButton(window, text = "+" , font=('consolas', 25), command=lambda: ExtraWindow().choice(1), width=35, height=25)
remove = CTkButton(window, text="-", font=('consolas', 25), command=lambda: ExtraWindow().choice(2), width=35, height=30)
Results = CTkButton(window, text="Spin", font=('consolas', 25), command=spin, corner_radius=32, hover_color="#4158D0")

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.columnconfigure(3, weight=1)
window.columnconfigure(4, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)

add.grid(row=0, column=0)
label1.grid(row=0, column=1, sticky="nsew")
label2.grid(row=0, column=2, sticky="nsew")
label3.grid(row=0, column=3, sticky="nsew")
remove.grid(row=0, column=4)
Results.grid(row=1, column=2, padx=20, pady=20)

window.mainloop()
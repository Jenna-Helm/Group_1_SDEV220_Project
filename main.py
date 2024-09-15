import tkinter as tk
from tkinter import ttk
import random as random

'''
========================================
=============Create classes=============
========================================
'''


class Person():
    
    # == base person class used for all people classes == 
    
    persons = [] # stores all objects that represent people. be it staff or other
    
    def __init__(self,fName,lName):
        self.fName = fName
        self.lName = lName

class Staff(Person):
    
    # == a subclass of person used for library staff ==

    def __init__(self,position,fName,lName):
        super().__init__(fName,lName) #bring in the first and last name from the parent class
        self.position = str(position)
        # self.staffId (the id should be generated when the object is created)
        # self.hireDate (the hire date should be generated when the object is created)
        # self.staffEmail (it may be better to provide the email, but in theory the system can make it. for now just a comment)

    @classmethod
    def add(cls,fName,lName,Position):
        pass
    
    def remove(self,staffId):
        pass

    @classmethod
    def list_all(cls):
        pass






'''
=====================================
=============Create data=============
=====================================
'''




'''
========================================
=============Create windows=============
========================================
'''

# create main window
root = tk.Tk()
root.geometry('400x150')
root.title("Library Systems")

#create buttons

#staff
staff_button = ttk.Button(
    root,
    text="Staff"
)
staff_button.pack(
    ipadx=5,
    ipady=5,
    side=tk.LEFT,
    expand=True
)

#media
invintory_button = ttk.Button(
    root,
    text="Invintory"
)
invintory_button.pack(
    ipadx=5,
    ipady=5,
    side=tk.LEFT,
    expand=True
)

#checkouts
checkout_ex_button = ttk.Button(
    root,
    text="Checkouts/existing"
)
checkout_ex_button.pack(
    ipadx=5,
    ipady=5,
    side=tk.LEFT,
    expand=True
)

#checkouts
checkout_new_button = ttk.Button(
    root,
    text="Checkouts/new"
)
checkout_new_button.pack(
    ipadx=5,
    ipady=5,
    side=tk.LEFT,
    expand=True
)


#checkouts new checkout
newCheckout = tk.Tk()
newCheckout.geometry('400x850')
newCheckout.title("New Checkout")



root.mainloop()
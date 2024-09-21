import tkinter as tk
from tkinter import ttk
import random as random
import Media_Class as mc
import Person_Class as pc
import Checkouts_Class as cc

# create a class for the root menu
class RootMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('400x150')
        self.title("Library Systems")

        
        #create buttons
        #staff
        staff_button = ttk.Button(
            self,
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
            self,
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
            self,
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
            self,
            text="Checkouts/new"
        )
        checkout_new_button.pack(
            ipadx=5,
            ipady=5,
            side=tk.LEFT,
            expand=True
        )
     
if __name__ == "__main__":
    #create the windows
    root = RootMenu() #Core window
    checkoutNew = cc.CheckoutNew()
    #checkoutNew.mainloop()

    #root.mainloop()

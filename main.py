import tkinter as tk
from tkinter import ttk
import random as random
import Media_Management as mc
import Person_Class as pc
import Checkouts_Class as cc

# create a class for the root menu
class RootMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('400x150')
        self.title("LibraryTraks Systems")

        #function to open MediaApp
        def open_media_app():
            app = mc.MediaApp(self)
            app.mainloop()
        #function to open staffApp
        def open_staff_app():
            app= pc.StaffApp(self)
            app.mainloop()

        #create buttons
        #staff
        staff_button = ttk.Button(
            self,
            text="Staff",
            command= open_staff_app
        )
        staff_button.pack(
            ipadx=5,
            ipady=5,
            side=tk.LEFT,
            expand=True
        )

        #media
        inventory_button = ttk.Button(
            self,
            text="Inventory",
            command = open_media_app #Bind command to function
        )
        inventory_button.pack(
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
    #checkoutNew = cc.CheckoutNew()
    #checkoutNew.mainloop()

    root.mainloop()

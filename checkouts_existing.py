import tkinter as tk
from tkinter import ttk
from tkinter import Text
import random, string
import datetime as time
from tkinter import messagebox
from configure import url_paths
import csv
import os


# create a class for the window
class CheckoutExistingNew(tk.Toplevel):

    def __init__(self):
        super().__init__()
        self.geometry("655x850")
        self.title("Existing Checkouts")

        #self.grid_rowconfigure(0, weight=1) 
        self.grid_columnconfigure(0, weight=1)

        #frame for the checkout list
        self.listFrame = ttk.LabelFrame(
            self,
            text="All checkouts"
        )
        self.listFrame.grid(column=0,row=0,sticky="nswe")

        self.checkoutList = ttk.Treeview(
            self.listFrame,
            columns=("Checkout ID","Due Date","Card Holder"),
            show="headings"
        )
        self.checkoutList.grid(column=0,row=0, sticky="nswe")
        # Column configuration 
        for col in self.checkoutList["columns"]:
            self.checkoutList.heading(col, text=col)
            self.checkoutList.column(col, width=100)


        #frame for the current checkout
        self.currentFrame = ttk.LabelFrame(
            self,
            text="Selected checkout"
        )
        self.currentFrame.grid(column=0,columnspan=2,row=4, rowspan=3,sticky="nswe")

        self.current_items_list = ttk.Treeview(
            self.currentFrame,
            columns=("ID", "Name", "Type", "Genre", "Author", "Serial Number", "Tags"),
            show="headings"
        )
        self.current_items_list.grid(column=0,columnspan=2,row=4, rowspan=3,sticky="nswe")
        # Column configuration 
        for col in self.current_items_list["columns"]:
            self.current_items_list.heading(col, text=col)
            self.current_items_list.column(col, width=70)

        # align items in the window
        self.listFrame.grid_rowconfigure(0, weight=1)
        self.listFrame.grid_columnconfigure(0, weight=1)
        self.currentFrame.grid_rowconfigure(0, weight=1)
        self.currentFrame.grid_columnconfigure(0, weight=1)

        #populate the checkouts
        self.populate_checkouts()

    #read all the files in the checkouts folder and populate the checkouts list
    def populate_checkouts(self):
        dir_list = os.listdir(url_paths["checkouts"])

        #loop through entries and add them to the treeview
        for item in dir_list:
            file = open(url_paths["checkouts"]+item)
            fileItems = file.readlines()
            fileItems = [line.strip() for line in fileItems if line.strip()]
            
            for inner in range(len(fileItems)):
                
                #get the card holder id
                if inner == 1:
                    check_card_holder = str(fileItems[inner]).strip().split(":")[1]
                    #print(f"line 0 = {fileItems[inner]}")
                    #check_card_holder = "place holder"

                #get the transaction ID
                if inner == 2:
                    #print(f"line 2 = {fileItems[inner]}")
                    check_id = str(fileItems[inner]).strip().split(":")[1]
                    #check_id = "place holder"

                #get the due date
                if inner == 3:
                    #print(f"line 4 = {fileItems[inner]}")
                    check_date = str(fileItems[inner]).strip().split(":")[1]
                    #check_date = "place holder"

                    #because the due date is the last item we need for this list.
                    #   we can add everything and break out of the loop
                    self.checkoutList.insert("","end",values=(check_id,check_date,check_card_holder) )

            '''
            self.checkoutList.insert("", "end", values=(item_data["ID"], item_data["Name"], item_data["Type"], item_data["Genre"], item_data["Author"], item_data["Serial Number"], item_data["Tags"]))    '''


# debug. make the window locally for rapid testing
if __name__ == "__main__":

    checkoutNew = CheckoutExistingNew()
    checkoutNew.mainloop()
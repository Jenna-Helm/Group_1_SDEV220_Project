import tkinter as tk
from tkinter import ttk
from tkinter import Text
import random, string
import datetime
from datetime import timedelta
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

        self.selected_checkout = tk.StringVar()
        self.checkoutList = ttk.Treeview(
            self.listFrame,
            columns=("Checkout ID","Due Date","Card Holder","fileName"),
            show="headings"
            #textvariable=self.selected_checkout
        )
        self.checkoutList.grid(column=0,row=0, sticky="nswe")
        # Column configuration 
        for col in self.checkoutList["columns"]:
            self.checkoutList.heading(col, text=col)
            self.checkoutList.column(col, width=100)

        #hide the fileName column
        self.checkoutList.column("fileName", width=0, stretch=tk.NO)


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

        self.checkoutList.bind('<<TreeviewSelect>>', lambda event: self.populate_checkout_items())
    
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

                #get the transaction ID
                if inner == 2:
                    check_id = str(fileItems[inner]).strip().split(":")[1]

                #get the due date
                if inner == 3:
                    duedate = str(fileItems[inner]).strip().split(":")[1]
                    
                    #if the item is over due flag it 
                    check_date = duedate.strip()
                    check_date = datetime.datetime.strptime(check_date, "%Y-%m-%d")
                    check_date = check_date.date()                                
                    current_date = datetime.datetime.now().date()
                   
                    # compare the dates and append if overdue
                    if check_date < (current_date - timedelta(days=1)):
                        #get the amount of days it is over
                        overdue_days = (current_date - check_date - timedelta(days=1)).days
                        duedate = f"{duedate} : (OVERDUE {overdue_days} days)"
                    #if due today append
                    print(f"formatted_date = {check_date}")
                    print(f"checkdate = {check_date}")
                    if check_date == (current_date - timedelta(days=1)):
                        duedate = f"{check_date} : (DUE TODAY)"

                    #because the due date is the last item we need for this list.
                    #   we can add everything and break out of the loop
                    self.checkoutList.insert("","end",values=(check_id,duedate,check_card_holder,item))

                file.close()


    def populate_checkout_items(self):

        selected_item = self.checkoutList.selection()
        file_name = self.checkoutList.item(selected_item,"values")[3]

        #remove any items already in the tree
        for item in self.current_items_list.get_children():
            self.current_items_list.delete(item)

        
        #read the file and populate the treeview
        file = open(url_paths["checkouts"]+file_name)
        for index,line in enumerate(file):
            
            #we only need to read the data related to the checkout
            if index >= 7:
                #print(line, end='')
                self.current_items_list.insert("", "end", values=line.strip().split(","))

                    
        file.close() 

    # show an error message
    def show_error(self,title,message):
        messagebox.showerror(title,message)

# debug. make the window locally for rapid testing
if __name__ == "__main__":

    checkoutNew = CheckoutExistingNew()
    checkoutNew.mainloop()
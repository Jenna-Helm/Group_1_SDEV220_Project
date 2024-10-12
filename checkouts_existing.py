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
import shutil
import checkouts_existing as ce

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
            columns=("ID", "Name", "Type", "Genre", "Author", "Serial Number", "Tags","Returned"),
            show="headings"
        )
        self.current_items_list.grid(column=0,columnspan=2,row=4, rowspan=3,sticky="nswe")
        
        #return button to restock the item
        self.return_button = tk.Button(
            self.currentFrame,
            text="Return to stock",
            command=self.return_item
        )
        self.return_button.grid(column=0,row=7)
        self.return_button.config(state="disabled")
        
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
        self.current_items_list.bind('<<TreeviewSelect>>', lambda event: self.populate_selected_checkout())

    #read all the files in the checkouts folder and populate the checkouts list
    def populate_checkouts(self):
        dir_list = os.listdir(url_paths["checkouts"])

        #remove any items already in the tree
        for item in self.checkoutList.get_children():
            self.checkoutList.delete(item)

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
                    if check_date < (current_date - timedelta(days=0)):
                        #get the amount of days it is over
                        overdue_days = (current_date - check_date - timedelta(days=0)).days
                        duedate = f"{duedate} : (OVERDUE {overdue_days} days)"
                    #if due today append
                    print(f"formatted_date = {check_date}")
                    print(f"checkdate = {check_date}")
                    if check_date == (current_date - timedelta(days=0)):
                        duedate = f"{check_date} : (DUE TODAY)"

                    #because the due date is the last item we need for this list.
                    #   we can add everything and break out of the loop
                    self.checkoutList.insert("","end",values=(check_id,duedate,check_card_holder,item))

                file.close()

    #read the file related to the selected checkout and populate the current items treeview
    def populate_checkout_items(self):

        #disable the return button
        self.return_button.config(state="disabled")

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

    #if a checked out item is selected. enable the return button
    def populate_selected_checkout(self):
        
        #enable the return button
        self.return_button.config(state="normal")

    # mark an item as being returned
    def return_item(self):
        
        #create a temporary list to store the file rewrite
        temp_data = []

        #create a test boolean that is set to True if all items are returned. else False
        returns_complete = True

        #get the selected row and the media item ID related to it.
        selected_row = self.current_items_list.selection()
        selected_item_id = self.current_items_list.item(selected_row, "values")[0]
        
        #get the file name related to the checkout
        file_name = self.checkoutList.item(self.checkoutList.selection(),"values")[3]    

        #prepare a temp file that matches the origonal. but replace the return status for the chosen item
        with open(url_paths["checkouts"]+file_name, 'r') as file:
            for line in file:
                #If the current line belongs to the selection, Modify the return state
                if line.split(",")[0] == selected_item_id:
                    line = str(line).replace("No","Yes")
                
                #test the line to see if it is No (not returned) if the item is not returned
                #   then the file needs to stay in current checkouts 
                if "No" in line:
                    returns_complete = False

                #write to the temp file
                temp_data.append(line)        

        file.close() 
        
        #rewrite the file 
        with open(url_paths["checkouts"]+file_name, 'w') as file:
            for item in temp_data:
                file.write(item)

        file.close()

        #set the item in stock boolean to true
        self.checkin_items(url_paths["media"],selected_item_id)

        #if all items are returned we need to move the file to the finished checkouts dirrectory 
        if returns_complete:
             
             #Before the file is moved. Append the end of it with the time of completion.
             file = open(url_paths["checkouts"]+file_name,"a")
             file.write(f"\n\nCheckout finished {datetime.datetime.now()}")
             file.close()

             source = url_paths["checkouts"]+file_name
             destination = url_paths["finished_checkouts"]+file_name
             dest = shutil.move(source,destination)
             self.Show_Info("Checkout Complete","All items are returned. file moved to completed checkouts")

             #reload all windows to remove the finished file from the treeview
             self.populate_checkouts()

            #clear the current_items_list 
             for item in self.current_items_list.get_children():
                self.current_items_list.delete(item)

        else:
            self.Show_Info("item Returned",f"item with ID {selected_item_id} returned.")

        #reopen the file to show the change
        self.populate_checkout_items()

    #change the in stock bolleon to True.
    def checkin_items(self,file_path,item_ID):
        
        # temp storage for the data
        temp_cvs = []
        
        if not os.path.exists(file_path):
            self.show_error("Bad path",f"Path '{url_paths['media']}' not found")
            return

        #loop through the items and update anything in the checkout
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["ID"] == item_ID:
                    #if the item is found check if it is in stock
                    row["In Stock"] = "Yes"
                    print(f"row {row}")
                
                #write the row to the temp cvs
                temp_cvs.append(row)   
        
        #write the file
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=temp_cvs[0].keys())
            writer.writeheader()
            writer.writerows(temp_cvs)

    # show an error message
    def show_error(self,title,message):
        messagebox.showerror(title,message)

    # show an success message
    def Show_Info(self,title,message):
        messagebox.showinfo(title,message)


# debug. make the window locally for rapid testing
if __name__ == "__main__":

    checkoutNew = CheckoutExistingNew()
    checkoutNew.mainloop()
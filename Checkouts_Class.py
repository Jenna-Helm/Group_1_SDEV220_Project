import tkinter as tk
from tkinter import ttk
from tkinter import Text
import random, string
import datetime as time
from tkinter import messagebox
from tkinter import *
from ttkwidgets.autocomplete import AutocompleteEntry
from configure import url_paths
import csv
import os



class CheckoutNew(tk.Toplevel):
    #How long until items must be returned in days
    checkout_time = 14

    #list of auto complete IDs for media
    auto_complete_media_ids = []
    #list of auto complete IDs for staff
    auto_complete_staff_ids = []
    #list of card holders
    auto_complete_card_holders = []
    #string of valid characters for entry
    valid_ID_characters = "abcdefghijklmnopqrstuvwxuyz1234567890"


    def __init__(self):
        super().__init__()
        self.geometry('655x850')
        self.title("New Checkout")

        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=1) 

        #generate a list of ID items for auocomplete
        self.make_autocomplete_card_holder_list()
        self.auto_complete_media_ids = self.make_autocomplete_list("media","ID")
        #self.make_autocomplete_list()
        self.make_autocomplete_staff_list() #staff list need their own function for now. but base function can be improved

        #checkout clerk. >>>>>>>>>
        clerk_name = ttk.LabelFrame(
            self,
            text="Clerk's name"
        )
        clerk_name.grid(column=0,row=0)

        self.staffid = tk.StringVar()
        self.checkNameInput = ttk.Combobox(
            clerk_name,
            height=1,
            width=20,
            textvariable=self.staffid
        )
        self.checkNameInput.grid(column=0,row=0)
        self.checkNameInput['values'] = self.auto_complete_staff_ids
        
        # checkout customer >>>>>>>

        card_holder_frame = ttk.LabelFrame(
            self,
            text="Card holders name"
        )
        card_holder_frame.grid(column=1,row=0)

        self.cardHolderNameInput = AutocompleteEntry(
            card_holder_frame,
            completevalues=self.auto_complete_card_holders,
        )
        self.cardHolderNameInput.grid(column=1,row=0)


        #create an add button. <<<<<<<<<<<<<<<<<<<<<<<<
        #frame to hold the checkout entry and button
        add_frame = ttk.LabelFrame(
            self,
            text="add by ID"
        )
        add_frame.grid(column=0,columnspan=2,row=4)

        self.add_fld = AutocompleteEntry(
            add_frame,
            completevalues=self.auto_complete_media_ids,
        )
        self.add_fld.grid(column=0,columnspan=2,row=4)
        self.add_fld.bind('<Return>', self.enter_pressed)

        add_butn = tk.Button(
            add_frame,
            text="Add",
            relief="raised",
            command=self.add_to_cart
        )
        add_butn.grid(column=3,row=4)
        
       
        # checkout list <<<<<<<<<<<<<<<<<<<<
        cart_frame = ttk.LabelFrame(
            self,
            text="Cart"
        )
        cart_frame.grid(column=0,columnspan=2,row=6)

        self.cart = ttk.Treeview(
            self,
            columns=("ID", "Name", "Type", "Genre", "Author", "Serial Number", "Tags"),
            show="headings"
        )
        #self.cart.heading(0,text="Serial Number")
        self.cart.grid(column=0,columnspan=2,row=6,sticky="nswe",padx=10,pady=5)
        # Column configuration 
        for col in self.cart["columns"]:
            self.cart.heading(col, text=col)
            self.cart.column(col, width=70)

        #add buttons to manage the cart
        cart_remove_button = tk.Button(
        self,
        text="Remove",
        command=self.remove_from_cart
        )
        cart_remove_button.grid(column=0,row=7)

        cart_finish = tk.Button(
            self,
            text="Checkout",
            command=self.finish_checkout
        )
        cart_finish.grid(column=1,row=7)



    # check if item exists
    def check_if_item_exists(self,file_path,column_name,target_item):
        if not os.path.exists(file_path):
            self.show_error("Bad path",f"Path '{url_paths['media']}' not found")
            return

        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row[column_name] == target_item:               
                    #if the item is found return all the data for it
                    return row
        return False



    #check if the item is in stock
    def check_if_item_in_stock(self,file_path,column_name,target_item):
        if not os.path.exists(file_path):
            self.show_error("Bad path",f"Path '{url_paths['media']}' not found")
            return

        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row[column_name] == target_item:               
                    #if the item is found check if it is in stock
                        if row.get("In Stock","Unknown") == "Yes":
                            return True
                        else:
                            return False
        return False



    #change the in stock bolleon to false.
    def checkout_items(self,file_path,item_list):
        
        # temp storage for the data
        temp_cvs = []
        
        if not os.path.exists(file_path):
            self.show_error("Bad path",f"Path '{url_paths['media']}' not found")
            return

        #loop through the items and update anything in the checkout
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["ID"] in item_list:               
                    #if the item is found check if it is in stock
                    row["In Stock"] = "No"
                
                #write the row to the temp cvs
                temp_cvs.append(row)      
        
        #write the file
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=temp_cvs[0].keys())
            writer.writeheader()
            writer.writerows(temp_cvs)
        


    #check if an item is already in the cart
    def check_cart_for_item(self, target_value):
        # go through the cart treeview
        for item_id in self.cart.get_children():
            item_values = self.cart.item(item_id)["values"]
            #test if the item matches
            if str(item_values[0]) == str(target_value):
                return True
        return False

    #If the enter key is used have it run the add
    #    to cart function as well as return a break to prevent
    #   a new line being added
    def enter_pressed(self,event):
        self.add_to_cart()
        return "break"

    #add an item to the cart
    def add_to_cart(self):       
    
        #check the entery box to make sure it has valid text
        if self.add_fld.get() == "":
            self.show_error("Entry Error","No ID in in the entry field.")
            return 

        #check entry for invalid characters
        for index in str(self.add_fld.get()).lower():
            if index not in self.valid_ID_characters:
                self.show_error("Entry Error","Invalid character in entry")
                return

        #store the item to add
        text = self.add_fld.get()

        #check the item exists
        item_data = self.check_if_item_exists(url_paths["media"],"ID",text)
        if not item_data:
            self.show_error("Error", f"No item with ID {text} exists.")
            return
        
        #check if the item is in stock
        if not self.check_if_item_in_stock(url_paths["media"],"ID",text):
            self.show_error("Entry Error", f"Item {text} is not in stock.")
            return

        #check if the item is already in the cart
        if self.check_cart_for_item(text):
            self.show_error("Entry Error", f"Item {text} is already in the cart.")
            return

        #If all tests pass add the item
        self.cart.insert("", "end", values=(item_data["ID"], item_data["Name"], item_data["Type"], item_data["Genre"], item_data["Author"], item_data["Serial Number"], item_data["Tags"]))        
        self.add_fld.delete(0,"end")


    def remove_from_cart(self):
        selected = self.cart.selection()
        if selected:
            for item in selected:
                self.cart.delete(item)
                
    def finish_checkout(self):
        
        #check the cart has items in it
        if len(self.cart.get_children()) == 0:
            self.show_error("Checkout error","No items in cart.")
            return

        #test that card holder and checkout clerck fields are populated
        if self.cardHolderNameInput.get() == "":
            self.show_error("Checkout error","No card holder ID entered.")
            return
        
        if self.staffid.get() == "":
            self.show_error("Checkout error","No staff ID entered.")
            return 
        
        #generate a random checkout number.
        checkout_num = str(self.generate_unique_id())
        checkout_time = str(time.datetime.now())
        formated_time = checkout_time.replace(".","-").replace(" ","-").replace(":","-")
        
        #make an empty list to hold item IDs for use in checkout_items
        id_list = []

        #make a file name using the time and a random code
        file_name = f'{formated_time} --- {checkout_num}'

        #print the checkout file name
        print(f'\n created checkout file {file_name}\n')

        #create a new checkout item
        file = open(f'{url_paths["checkouts"]}{file_name}.txt', 'w')

        #write the clerk and card holders name to the file
        file.write(f'Checkout clerk : {self.staffid.get()} \n')
        file.write(f'Card holder number : {self.cardHolderNameInput.get()} \n')
        file.write(f'Checkout ID : {checkout_num} \n')

        #write when items must be returned
        return_by = str(time.datetime.now() + time.timedelta(days=self.checkout_time)).split()[0]
        file.write(f'Return by date : {return_by} \n\n')

        #write an open bracket for items checkedout 
        file.write("Items checkedout >>>>>>>>>>>>>>>>\n")
        
        #create a temporary list to store each entry and write to it.
        file.write(f"{str(self.cart['columns'])},Returned\n")
        for index, row_id in enumerate(self.cart.get_children()):
            
            # add the ID to a list to use in checkout_items
            id_list.append(self.cart.item(row_id)["values"][0])

            row = self.cart.item(row_id)["values"]

            # Convert the row values to a string without brackets and quotes
            row_str = ', '.join(map(str, row))  # Join values as a comma-separated string
            
            #write the line
            file.write(f"{str(row_str)},No")

            #if we are on the last line we do not need a new space
            if index != len(self.cart.get_children())-1:
                file.write(f"\n")
            
        #close the file
        file.close()

        self.Show_Info("success","Checkout File made.")
        self.destroy()

        #update the invintory to display the items checked out
        self.checkout_items(url_paths["media"],id_list)



     # populate the auto complete list
    def make_autocomplete_list(self,path_url,row_name):
        
        list_data = []

        with open(url_paths[path_url], newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                list_data.append(row[row_name])
        
        return list_data



    def make_autocomplete_list_staff(self):
        
        with open(url_paths["media"], newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.auto_complete_ids.append(row["ID"])
        


    def make_autocomplete_staff_list(self):
        with open(url_paths["staff"], newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                first = str(row["First Name"])
                last = str(row["Last Name"])
                ID = str(row["Staff ID"])
                self.auto_complete_staff_ids.append(str(f' {first} {last} ({ID})'))
   


    def make_autocomplete_card_holder_list(self):
        with open(url_paths["cardHolders"], newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                first = str(row["fName"])
                last = str(row["lName"])
                ID = str(row["ID"])
                self.auto_complete_card_holders.append(str(f' {first} {last} ({ID})'))



    # Generates 5 digit unique id   
    @staticmethod
    def generate_unique_id(length=5):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    


    # show an error message
    def show_error(self,title,message):
        messagebox.showerror(title,message)



        # show an success message
    def Show_Info(self,title,message):
        messagebox.showinfo(title,message)



# debug. make the window locally for rapid testing
if __name__ == "__main__":
    checkoutNew = CheckoutNew()
    checkoutNew.mainloop()
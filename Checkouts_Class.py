import tkinter as tk
from tkinter import ttk
from tkinter import Text
import random, string
import datetime as time

class CheckoutNew(tk.Tk):
    #How long until items must be returned in days
    checkout_time = 14
    
    def __init__(self):
        super().__init__()
        self.geometry('655x850')
        self.title("New Checkout")

        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=1) 

        #checkout clerk. >>>>>>>>>
        clerk_name = ttk.LabelFrame(
            self,
            text="Clerk's name"
        )
        clerk_name.grid(column=0,row=0)

        self.checkNameInput = Text(
            clerk_name,
            height=1,
            width=20,
            relief="raised"
        )
        self.checkNameInput.grid(column=0,row=0)
        self.checkNameInput.insert(1.0,"Lizzy") #place holder name. 
        
        # checkout customer >>>>>>>

        card_holder_frame = ttk.LabelFrame(
            self,
            text="Card holders name"
        )
        card_holder_frame.grid(column=1,row=0)

        self.cardHolderNameInput = Text(
            card_holder_frame,
            height=1,
            width=20,
            relief="raised"
        )
        self.cardHolderNameInput.grid(column=1,row=0)
        self.cardHolderNameInput.insert(1.0,"Bob") #place holder name. 

        #create an add button. <<<<<<<<<<<<<<<<<<<<<<<<
        #frame to hold the checkout entry and button
        add_frame = ttk.LabelFrame(
            self,
            text="add by serial"
        )
        add_frame.grid(column=0,columnspan=2,row=4)

        self.add_fld = Text(
            add_frame,
            height=1,
            width=25
        )
        self.add_fld.grid(column=0,columnspan=2,row=4)
        
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
            columns=("Serial num")
        )
        self.cart.heading(0,text="Serial Number")
        self.cart.grid(column=0,columnspan=2,row=6)

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

    #add an item to the cart
    def add_to_cart(self):       
    
        text = self.add_fld.get(1.0,"end-1c")
        self.cart.insert("","end",values=(text))        
        self.add_fld.delete(1.0,"end")

    def remove_from_cart(self):
        selected = self.cart.selection()
        if selected:
            self.cart.delete(selected)

    def finish_checkout(self):
        #generate a random checkout number.
        checkout_num = str(self.generate_unique_id())
        checkout_time = str(time.datetime.now())
        formated_time = checkout_time.replace(".","-").replace(" ","-").replace(":","-")
        
        #make a file name using the time and a random code
        file_name = f'{formated_time} --- {checkout_num}'

        #print the checkout file name
        print(f'\n created checkout file {file_name}\n')

        #create a new checkout item
        file = open(f'./checkouts/{file_name}.txt', 'w')

        #write the clerk and card holders name to the file
        file.write(f'Checkout clerk : {self.checkNameInput.get(1.0,"end-1c")} \n')
        file.write(f'Card holder number : {self.cardHolderNameInput.get(1.0,"end-1c")} \n \n')

        #write when items must be returned
        return_by = str(time.datetime.now() + time.timedelta(days=self.checkout_time)).split()[0]
        file.write(f'Return by date : {return_by} \n \n')

        file.write("Items checkedout >>>>>>>>>>>>>>>>\n")
        #write the items to the checkout text file
        for item in self.cart.get_children():
            item_values = self.cart.item(item, 'values')
            item_str = ' '.join(item_values)
            file.write(f'item //  {item_str} \n')
        
        file.write("Items checkedout <<<<<<<<<<<<<<<<\n")

        file.close()

    # Generates 5 digit unique id   
    @staticmethod
    def generate_unique_id(length=5):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))



# debug. make the window locally for rapid testing
if __name__ == "__main__":
    checkoutNew = CheckoutNew()
    checkoutNew.mainloop()
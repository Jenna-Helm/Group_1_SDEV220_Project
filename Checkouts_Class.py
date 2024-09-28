import tkinter as tk
from tkinter import ttk
from tkinter import Text


class CheckoutNew(tk.Tk):
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

        checkNameInput = Text(
            clerk_name,
            height=1,
            width=20,
            relief="raised"
        )
        checkNameInput.grid(column=0,row=0)
        checkNameInput.insert(1.0,"Lizzy") #place holder name. 
        
        # checkout customer >>>>>>>

        card_holder_frame = ttk.LabelFrame(
            self,
            text="Card holders name"
        )
        card_holder_frame.grid(column=1,row=0)

        cardHolderNameInput = Text(
            card_holder_frame,
            height=1,
            width=20,
            relief="raised"
        )
        cardHolderNameInput.grid(column=1,row=0)
        cardHolderNameInput.insert(1.0,"Bob") #place holder name. 

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
        file = open("checkouts/checkout.text","w")

        for item in self.cart.get_children():
            file.write(str(self.cart.item(item, 'values')))

        file.close()



# debug. make the window locally for rapid testing
if __name__ == "__main__":
    checkoutNew = CheckoutNew()
    checkoutNew.mainloop()
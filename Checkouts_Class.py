import tkinter as tk
from tkinter import ttk
from tkinter import Text


class CheckoutNew(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('400x850')
        self.title("New Checkout")

        #make a grid for easy placement
        #self.columnconfigure(padx=10)
        #self.rowconfigure(3)
        
        #buttons
        checkNameLabel = tk.Label(
            self,
            text="Cleark name:",
            relief="raised"
        )
        checkNameLabel.grid(column=0,row=0)

        checkNameInput = Text(
            self,
            height=1,
            relief="raised"
        )
        checkNameInput.grid(column=1,row=0)
        checkNameInput.insert(1.0,"Lizzy") #place holder name. 

        #create a seperator
        separator = ttk.Separator(self, orient='horizontal')
        separator.grid(column=1,row=2,columnspan=3,ipady=5)



# debug. make the window locally for rapid testing
if __name__ == "__main__":
    checkoutNew = CheckoutNew()
    checkoutNew.mainloop()
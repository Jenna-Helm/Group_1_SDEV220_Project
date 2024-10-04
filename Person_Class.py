import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random, string, csv, os

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LibraryTraks Management")
        self.geometry("800x600")

        # Create Notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Add StaffApp and CardHolderApp tabs
        self.staff_app = StaffApp(self.notebook)
        self.cardholder_app = CardHolderApp(self.notebook)

        self.notebook.add(self.staff_app, text="Manage Staff")
        self.notebook.add(self.cardholder_app, text="Manage CardHolders")


class Person():
    # base person class
    persons = []  # stores all objects that represent people

    def __init__(self, fName, lName):
        self.fName = fName
        self.lName = lName

class Staff(Person):
    # subclass of person used for library staff
    staff_list = []  # Staff list for storing staff instances

    def __init__(self, position, fName, lName):
        super().__init__(fName, lName)  # bring in the first name and last name from the parent class
        self.position = str(position)
        self.staffId = self.generate_unique_id()
        self.staff_list.append(self)

    @staticmethod
    def generate_unique_id(length=8):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def print_details(self):
        details = (
            f"Staff ID: {self.staffId}\n"
            f"First Name: {self.fName}\n"
            f"Last Name: {self.lName}\n"
            f"Position: {self.position}\n"
        )
        print(details)

    @classmethod
    def add(cls, fName, lName, position):  # adding a new staff member
        new_staff = cls(position, fName, lName)  # used to create a new instance
        print(f"Added Staff: {new_staff.fName} {new_staff.lName}, ID: {new_staff.staffId}, Position: {new_staff.position}")

    @classmethod
    def remove(cls, staffId):  # removing a staff member
        for staff in cls.staff_list:
            if staff.staffId == staffId:  # If staff is found
                cls.staff_list.remove(staff)  # Removes staff member from the appended list
                print(f"Removed Staff: {staff.fName} {staff.lName}, ID: {staffId}")
                return
        print(f"No Staff found with the ID: {staffId}")  # if staff is not found

    @classmethod
    def list_all(cls):
        if not cls.staff_list:
            print("No staff members found.")
            return
        print("List of Active Staff Members:")
        for staff in cls.staff_list:
            print(f"ID: {staff.staffId}, Name: {staff.fName} {staff.lName}, Position: {staff.position}")

# Tkinter GUI functions
class StaffApp(tk.Toplevel):  # Changed back to Toplevel to bind button on Main
    def __init__(self, parent):
        super().__init__(parent)
        self.title("LibraryTraks Staff Management")
        self.geometry('600x400')
        self.staff_list = []

        # Initialize widgets
        self.form_frame = ttk.LabelFrame(self, text="Add New Staff")
        self.staffId_entry = ttk.Entry(self.form_frame)
        self.fName_entry = ttk.Entry(self.form_frame)
        self.lName_entry = ttk.Entry(self.form_frame)
        self.position_entry = ttk.Entry(self.form_frame)
        self.add_button = ttk.Button(self.form_frame, text="Add Staff", command=self.add_staff)
        self.load_button = ttk.Button(self, text="Load Staff from File", command=self.load_staff_from_file_dialog, width=20)
        self.list_frame = ttk.LabelFrame(self, text="Staff List")
        self.tree = ttk.Treeview(self.list_frame, columns=("ID", "First Name", "Last Name", "Position"), show="headings")
        self.delete_button = ttk.Button(self, text="Delete Selected", command=self.delete_selected_staff)
        self.save_close_button = ttk.Button(self, text="Save & Close", command=self.save_and_close)

        self.create_widgets()
        self.load_staff_from_file('staff_data.csv')

    def create_widgets(self):
        # Add Staff
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Staff ID Labels
        self.id_label = ttk.Label(self.form_frame, text="Staff ID:")
        self.id_value = ttk.Label(self.form_frame, text="")
        self.id_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.id_value.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.form_frame, text="First Name:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.fName_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.form_frame, text="Last Name:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.lName_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.form_frame, text="Position:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.position_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Button loading staff
        self.add_button.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        # Grid to display staff 
        self.list_frame.grid(row=10, column=0, padx=10, pady=10, sticky="nsew")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)

        # Column configuration 
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.delete_button.grid(row=11, column=0, padx=5, pady=5, sticky="ew")
        self.save_close_button.grid(row=12, column=0, padx=5, pady=5, sticky="e")
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def add_staff(self):
        fName = self.fName_entry.get()
        lName = self.lName_entry.get()
        position = self.position_entry.get()

        if not fName or not lName or not position:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return

        new_staff = Staff(position, fName, lName)
        self.staff_list.append(new_staff)
        new_staff.print_details()

        # Update the unique ID label
        self.id_value.config(text=new_staff.staffId)

        # Add to treeview
        self.tree.insert("", "end", values=(new_staff.staffId, fName, lName, position))

        # Clear the form
        self.fName_entry.delete(0, tk.END)
        self.lName_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)

    def load_staff_from_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.load_staff_from_file(file_path)

    def load_staff_from_file(self, file_path):
        if not os.path.exists(file_path):
            messagebox.showerror("File Error", "File does not exist.")
            return
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                fName = row.get('First Name', 'Unknown')
                lName = row.get('Last Name', 'Unknown')
                position = row.get('Position', 'Unknown')

                new_staff = Staff(position, fName, lName)
                self.staff_list.append(new_staff)
                new_staff.print_details()

                # Add to treeview
                self.tree.insert("", "end", values=(new_staff.staffId, fName, lName, position))

    def delete_selected_staff(self):  # Deleting the selected staff
        selected_items = self.tree.selection()
        for item in selected_items:
            # Remove the staff from the staff list as well
            staff_id = self.tree.item(item)['values'][0]  # Get the staff ID from the selected item
            Staff.remove(staff_id)  # Remove from staff list
            self.tree.delete(item)  # Delete from the treeview

    def save_and_close(self):  # Choose to just allow a save and close for now
        self.save_staff_to_file('staff_data.csv')
        self.destroy()

    def save_staff_to_file(self, file_path):
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['Staff ID', 'First Name', 'Last Name', 'Position']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for staff in self.staff_list:
                writer.writerow({
                    'Staff ID': staff.staffId,
                    'First Name': staff.fName,
                    'Last Name': staff.lName,
                    'Position': staff.position,
                })

#Cardholder By Sean Kennedy //Added 10/03/2024

# CardHolder subclass
class CardHolder(Person):
    cardholder_list = []

    def __init__(self, membership_type, fName, lName):
        super().__init__(fName, lName)
        self.membership_type = str(membership_type)
        self.card_id = self.generate_unique_id()
        self.cardholder_list.append(self)

    @staticmethod
    def generate_unique_id(length=8):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def print_details(self):
        details = (
            f"Card ID: {self.card_id}\n"
            f"First Name: {self.fName}\n"
            f"Last Name: {self.lName}\n"
            f"Membership Type: {self.membership_type}\n"
        )
        print(details)

    @classmethod
    def add(cls, fName, lName, membership_type):
        new_cardholder = cls(membership_type, fName, lName)
        print(f"Added CardHolder: {new_cardholder.fName} {new_cardholder.lName}, ID: {new_cardholder.card_id}, Membership Type: {new_cardholder.membership_type}")

    @classmethod
    def remove(cls, card_id):
        for cardholder in cls.cardholder_list:
            if cardholder.card_id == card_id:
                cls.cardholder_list.remove(cardholder)
                print(f"Removed CardHolder: {cardholder.fName} {cardholder.lName}, ID: {card_id}")
                return
        print(f"No CardHolder found with the ID: {card_id}")

    @classmethod
    def list_all(cls):
        if not cls.cardholder_list:
            print("No cardholders found.")
            return
        print("List of Active Card Holders:")
        for cardholder in cls.cardholder_list:
            print(f"ID: {cardholder.card_id}, Name: {cardholder.fName} {cardholder.lName}, Membership Type: {cardholder.membership_type}")

# Tkinter GUI for managing cardholders
class CardHolderApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("LibraryTraks CardHolder Management")
        self.geometry('650x500')
        self.cardholder_list = []

        # Initialize widgets
        self.form_frame = ttk.LabelFrame(self, text="Add New CardHolder")
        self.card_id_label = ttk.Label(self.form_frame, text="Card ID:")
        self.card_id_value = ttk.Label(self.form_frame, text="")
        self.fName_entry = ttk.Entry(self.form_frame)
        self.lName_entry = ttk.Entry(self.form_frame)
        self.membership_type_entry = ttk.Entry(self.form_frame)
        self.add_button = ttk.Button(self.form_frame, text="Add CardHolder", command=self.add_cardholder)
        self.list_frame = ttk.LabelFrame(self, text="CardHolder List")
        self.tree = ttk.Treeview(self.list_frame, columns=("ID", "First Name", "Last Name", "Membership Type"), show="headings")
        self.delete_button = ttk.Button(self, text="Delete Selected", command=self.delete_selected_cardholder)

        self.create_widgets()

    def create_widgets(self):
        # Add CardHolder
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Card ID Labels
        self.card_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.card_id_value.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.form_frame, text="First Name:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.fName_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.form_frame, text="Last Name:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.lName_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.form_frame, text="Membership Type:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.membership_type_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Add button
        self.add_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        # CardHolder List
        self.list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Treeview column configuration
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Delete button
        self.delete_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # Configure weights
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def add_cardholder(self):
        fName = self.fName_entry.get()
        lName = self.lName_entry.get()
        membership_type = self.membership_type_entry.get()

        if not fName or not lName or not membership_type:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return

        new_cardholder = CardHolder(membership_type, fName, lName)
        self.cardholder_list.append(new_cardholder)
        new_cardholder.print_details()

        # Update the unique ID label
        self.card_id_value.config(text=new_cardholder.card_id)

        # Add to treeview
        self.tree.insert("", "end", values=(new_cardholder.card_id, fName, lName, membership_type))

        # Clear the form
        self.fName_entry.delete(0, tk.END)
        self.lName_entry.delete(0, tk.END)
        self.membership_type_entry.delete(0, tk.END)

    def delete_selected_cardholder(self):
        selected_items = self.tree.selection()
        for item in selected_items:
            card_id = self.tree.item(item)['values'][0]
            CardHolder.remove(card_id)
            self.tree.delete(item)

# Main loop
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    app = CardHolderApp(root)
    app.mainloop()

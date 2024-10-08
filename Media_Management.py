
import random, string
import tkinter as tk
from tkinter import ttk, filedialog
import csv, os

class Media:
    def __init__(self, unique_id,name, media_type, genre, author, serial_num, in_stock, tags):
        self.name = name
        self.media_type = media_type
        self.genre = genre
        self.author = author
        self.unique_id = unique_id
        self.serial_num = serial_num
        self.in_stock = in_stock
        self.tags = tags

    @staticmethod
    def generate_unique_id(length=8):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def print_details(self):
        details = (
            f"ID: {self.unique_id}"
            f"Name: {self.name}\n"
            f"Type: {self.media_type}\n"
            f"Genre: {self.genre}\n"
            f"Author: {self.author}\n"
            f"ID: {self.unique_id}\n"
            f"Serial Number: {self.serial_num}\n"
            f"In Stock: {'Yes' if self.in_stock else 'No'}\n"
            f"Tags: {', '.join(self.tags)}"
        )
        print(details)

class MediaApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("LibraryTraks Media Management")
        self.geometry('875x675')
        self.media_list = []

        # Initialize widgets
        self.form_frame = ttk.LabelFrame(self, text="Add New Media")
        self.name_entry = ttk.Entry(self.form_frame)
        self.type_entry = ttk.Entry(self.form_frame)
        self.genre_entry = ttk.Entry(self.form_frame)
        self.author_entry = ttk.Entry(self.form_frame)
        self.serial_entry = ttk.Entry(self.form_frame)
        self.in_stock_var = tk.BooleanVar()
        self.in_stock_check = ttk.Checkbutton(self.form_frame, variable=self.in_stock_var)
        self.tags_entry = ttk.Entry(self.form_frame)
        self.add_button = ttk.Button(self.form_frame, text="Add Media", command=self.add_media)
        self.load_button = ttk.Button(self, text="Load Media from File", command=self.load_media_from_file_dialog, width=20)
        self.list_frame = ttk.LabelFrame(self, text="Media List")
        self.tree = ttk.Treeview(self.list_frame, columns=("ID", "Name", "Type", "Genre", "Author", "Serial Number", "In Stock", "Tags"), show="headings")
        self.delete_button = ttk.Button(self, text="Delete Selected", command=self.delete_selected_media)
        self.save_close_button = ttk.Button(self, text="Save & Close", command=self.save_and_close)

        self.create_widgets()
        self.load_media_from_file('media_data.csv')

    def create_widgets(self):
        # Form to add new media
        self.form_frame.grid(row=0, column=0, padx=15, pady=5, sticky="ew")

        # Unique ID Label
        self.id_label = ttk.Label(self.form_frame, text="ID:")
        self.id_value = ttk.Label(self.form_frame, text="")
        self.id_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")  
        self.id_value.grid(row=0, column=1, padx=5, pady=5, sticky="w")  

        ttk.Label(self.form_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e") 
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")  
        self.name_entry.config(width=30)  

        ttk.Label(self.form_frame, text="Type:").grid(row=2, column=0, padx=5, pady=5, sticky="e") 
        self.type_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")  
        self.type_entry.config(width=30)  

        ttk.Label(self.form_frame, text="Genre:").grid(row=3, column=0, padx=5, pady=5, sticky="e")  
        self.genre_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w") 
        self.genre_entry.config(width=30)  

        ttk.Label(self.form_frame, text="Author:").grid(row=4, column=0, padx=5, pady=5, sticky="e")  
        self.author_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")  
        self.author_entry.config(width=30)  

        ttk.Label(self.form_frame, text="Serial Number:").grid(row=5, column=0, padx=5, pady=5, sticky="e")  
        self.serial_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")  
        self.serial_entry.config(width=30)  

        ttk.Label(self.form_frame, text="In Stock:").grid(row=6, column=0, padx=5, pady=5, sticky="e")  
        self.in_stock_check.grid(row=6, column=1, padx=5, pady=5, sticky="w")  

        ttk.Label(self.form_frame, text="Tags:").grid(row=7, column=0, padx=5, pady=5, sticky="e")  
        self.tags_entry.grid(row=7, column=1, padx=5, pady=5, sticky="w")  
        self.tags_entry.config(width=30)  

        self.add_button.grid(row=8, column=0, padx=5, pady=5)
        
        # **Add search entry and button**
        self.search_entry = ttk.Entry(self)
        self.search_entry.grid(row=9, column=0, padx=5, pady=5, sticky="se")
        self.search_entry.config(width=75)

        self.search_button = ttk.Button(self, text="Search", command=self.search_media)
        self.search_button.grid(row=9, column=0, padx=5, pady=5, sticky="en")

        # Button to load media from file
        self.load_button.grid(row=9, column=0, padx=5, pady=5, sticky="w") 

        # Grid to display media
        self.list_frame.grid(row=10, column=0, padx=10, pady=10, sticky="nsew")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=2)

        # Column configuration 
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, anchor="w")  
            if col == "Name":
                self.tree.column(col, width=150, anchor="w") 
            elif col == "In Stock":
                self.tree.column(col, width=60, anchor="w")  
            else:
                self.tree.column(col, width=100, anchor="w")  

        self.delete_button.grid(row=11, column=0, padx=5, pady=5, sticky="e")
        self.save_close_button.grid(row=12, column=0, padx=5, pady=5, sticky="e")
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        
        #scroll bar for media
        self.scrollBar = ttk.Scrollbar(
            self.list_frame,
            orient='vertical',
            command=self.tree.yview
        )
        self.scrollBar.grid(row=0, column=1, padx=5, pady=5,sticky="ns")
        # Configure the Treeview to use the scrollbar
        self.tree.configure(yscrollcommand=self.scrollBar.set)

    def add_media(self):
        unique_id = Media.generate_unique_id()
        name = self.name_entry.get()
        media_type = self.type_entry.get()
        genre = self.genre_entry.get()
        author = self.author_entry.get()
        serial_num = self.serial_entry.get()
        in_stock = self.in_stock_var.get()
        tags = self.tags_entry.get().split(',')

        new_media = Media(unique_id, name, media_type, genre, author, serial_num, in_stock, tags)
        self.media_list.append(new_media)
        new_media.print_details()

        # Update the unique ID label
        self.id_value.config(text=new_media.unique_id)

        # Add to treeview
        self.tree.insert("", "end", values=(new_media.unique_id, name, media_type, genre, author, serial_num, "Yes" if in_stock else "No", ", ".join(tags)))

        # Clear the form
        self.name_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.serial_entry.delete(0, tk.END)
        self.in_stock_var.set(False)
        self.tags_entry.delete(0, tk.END)
        

    def load_media_from_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.load_media_from_file(file_path)

    def load_media_from_file(self, file_path):
        if not os.path.exists(file_path):
            return
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                unique_id = row.get('ID', 'Unknown')
                name = row.get('Name', 'Unknown')
                media_type = row.get('Type', 'Unknown')
                genre = row.get('Genre', 'Unknown')
                author = row.get('Author', 'Unknown')
                serial_num = row.get('Serial Number', 'Unknown')
                in_stock = row.get('In Stock', 'no').lower() == 'yes'
                tags = row.get('Tags', '').split(',')

                new_media = Media(unique_id, name, media_type, genre, author, serial_num, in_stock, tags)
                self.media_list.append(new_media)
                new_media.print_details()

                # Add to treeview
                self.tree.insert("", "end", values=(unique_id, name, media_type, genre, author, serial_num, "Yes" if in_stock else "No", ", ".join(tags)))

    def delete_selected_media(self):
        selected_items = self.tree.selection()
        for item in selected_items:
            self.tree.delete(item)

    def save_and_close(self):
        self.save_media_to_file('media_data.csv')
        self.destroy()

    def save_media_to_file(self, file_path):
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Name', 'Type', 'Genre', 'Author', 'Serial Number', 'In Stock', 'Tags']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for media in self.media_list:
                writer.writerow({
                    'ID': media.unique_id,
                    'Name': media.name,
                    'Type': media.media_type,
                    'Genre': media.genre,
                    'Author': media.author,
                    'Serial Number': media.serial_num,
                    'In Stock': 'Yes' if media.in_stock else 'No',
                    'Tags': ', '.join(media.tags)
                })
    def search_media(self):
        query = self.search_entry.get().lower()
        results = [media for media in self.media_list if query in media.name.lower() or query in media.media_type.lower() or query in media.genre.lower() or query in media.author.lower() or query in media.serial_num.lower() or any(query in tag.lower() for tag in media.tags)]

        for row in self.tree.get_children():
            self.tree.delete(row)

        for media in results:
            self.tree.insert("", "end", values=(media.unique_id, media.name, media.media_type, media.genre, media.author, media.serial_num, media.in_stock, ', '.join(media.tags)))

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaApp(root)
    root.mainloop()
# Bones/Start of Media Class
import random, string
import tkinter as tk
from tkinter import ttk

class Media:
    def __init__(self, name, media_type, genre, author, serial_num, in_stock, tags):
        self.name = name
        self.media_type = media_type #Book, Magazine, CD, DVD, etc.
        self.genre = genre
        self.author = author
        self.unique_id = self.generate_unique_id() #function to generate unique id
        self.serial_num= serial_num
        self.in_stock = in_stock
        self.tags = tags                             

    # Generates 5 digit unique id   
    @staticmethod
    def generate_unique_id(length=5):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    # Prints report of media item
    def print_details(self):
        details = (
            f"Name: {self.name}\n"
            f"Type: {self.media_type}\n"
            f"Genre: {self.genre}\n"
            f"Author: {self.author}\n"
            f"ID: {self.unique_id}\n"
            f"Serial Number: {self.serial_num}\n"
            f"In Stock: {'Yes' if self.in_stock else 'No'}\n"
            f"Tags: {', '.join(self.tags)}"
        )

    # Method to add new media items    
    @classmethod
    def add_new_media(cls):
        name = input("Enter the name of the media: ")
        media_type = input("Enter the type of media (Book, Magazine, CD, DVD): ")
        genre = input("Enter the main genre of the media: ")
        author = input("Enter the author of the media: ")
        serial_num = input("Enter the serial number of the media: ")
        in_stock = input("Is the media in stock? (yes/no): ").lower() == 'yes'
        tags = input("Enter tags for the media (comma-separated): ").split(',')
        tags = [tag.strip() for tag in tags]  # Remove any extra whitespace
    
        # Generate unique_id when adding new media
        unique_id = cls.generate_unique_id()
    
        return cls(name, media_type, genre, author, unique_id, serial_num, in_stock, tags)



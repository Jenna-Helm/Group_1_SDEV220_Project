# Bones/Start of Media Class
import random, string

class Media:
    def __init__(self, name, media_type, genre, author, in_stock, tags):
        self.name = name
        self.media_type = media_type #Book, Magazine, CD, DVD, etc.
        self.genre = genre
        self.author = author
        self.serial_num = self.generate_serial_num() #function to generate serial number
        self.in_stock = in_stock
        self.Tags = tags                             

    # Generates 8 digit serial number    
    def generate_serial_num(self, length=8):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    # Prints report of media item
    def print_details(self):
        details = (
            f"Name: {self.name}\n"
            f"Type: {self.media_type}\n"
            f"Genre: {self.genre}\n"
            f"Author: {self.author}\n"
            f"Serial Number: {self.serial_num}\n"
            f"In Stock: {'Yes' if self.in_stock else 'No'}\n"
            f"Tags: {', '.join(f'{key}: {value}' for key, value in self.tags.items())}"
        )
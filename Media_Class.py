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
        self.tags = tags                             

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

    # Method to add new media items    
    @classmethod
    def add_new_media(cls):
        name = input("Enter the name of the media: ")
        media_type = input("Enter the type of media (Book, Magazine, CD, DVD): ")
        genre = input("Enter the main genre of the media: ")
        author = input("Enter the author of the media: ")
        in_stock = input("Is the media in stock? (yes/no): ").lower() == 'yes' #not sure if this redundent or not. if were adding wouldn't it be in stock?
        tags = {}
        while True:
            key = input("Enter a tag key (or 'done' to finish): ")
            if key.lower() == 'done':
                break
            value = input(f"Enter the value for tag '{key}': ")
            tags[key] = value
        # not sure what exactly we will add here. Maybe things like condition: new or cut: Director's
        # key will store the first, value stores the second.
        return cls(name, media_type, genre, author, in_stock, tags)
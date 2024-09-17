# Bones/Start of Media Class
import random, string

class Media:
    def __init__(self, title, media_type, genre, author, in_stock, tags):
        self.title = title
        self.media_type = media_type #Book, Magazine, CD, DVD, etc.
        self.genre = genre
        self.author = author
        self.serial_num = self.generate_serial_num() #function to generate serial number
        self.in_stock = in_stock
        self.Tags = tags                             

    # Generates 8 digit serial number    
    def generate_serial_num(self, length=8):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

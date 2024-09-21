import tkinter as tk
from tkinter import ttk

class Person():
    
    # == base person class used for all people classes == 
    
    persons = [] # stores all objects that represent people. be it staff or other
    
    def __init__(self,fName,lName):
        self.fName = fName
        self.lName = lName

class Staff(Person):
    
    # == a subclass of person used for library staff ==

    def __init__(self,position,fName,lName):
        super().__init__(fName,lName) #bring in the first and last name from the parent class
        self.position = str(position)
        # self.staffId (the id should be generated when the object is created)
        # self.hireDate (the hire date should be generated when the object is created)
        # self.staffEmail (it may be better to provide the email, but in theory the system can make it. for now just a comment)

    @classmethod
    def add(cls,fName,lName,Position):
        pass
    
    def remove(self,staffId):
        pass

    @classmethod
    def list_all(cls):
        pass







'''
========================================
=============Create windows=============
========================================
'''




'''
==========================================
=============Create functions=============
==========================================
'''


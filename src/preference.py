#preference.py
#----------------------------------
# Created By: Savannah Stephenson
# Created Date: 9/24/2023
#----------------------------------
# Edited By: Savannah Stephenson
# Edit Date: 10/18/2023
# Notes: Maybe add a note for how the min and max price should be entered or a way to validate input? 
# Edited By: Savannah Stephenson
# Edit Date: 10/18/2023
# Notes: Maybe add a note for how the min and max price should be entered or a way to validate input? 
#----------------------------------
"""This file asks and sets the user's preferences.  
 """ 
#----------------------------------
# 
#Imports
import tkinter
from tkinter import * 
from tkinter.ttk import *
from tkinter import ttk

class Preferences():
    ''' The Preferences class that holds the user's preferences. Includes location, listing type, property type, min price, max price, min beds, max beds, and min baths.
    '''
    def __init__(self) -> None:
        ''' Constructor for Preferences Class. Sets Location to Corpus-Christi and other values to default empty. 
        '''
        self.location = 'Corpus-Christi'
        self.listing_type = ' '
        self.property_type = ' '
        self.min_price = ''
        self.max_price = ''
        self.min_beds = ''
        self.max_beds = ''
        self.min_baths = ''

    def set_listing_type_field(self, listing_type: int):
       ''' Function to set listing type
       '''
       self.listing_type = listing_type
    

    def set_property_type_field(self, property_type: str):
        ''' Function to set property type
       '''
        self.property_type = property_type

    def set_min_price_entry_field(self, min_price: str):
        ''' Function to set min price
       '''
        self.min_price = min_price
    
    def set_max_price_entry_field(self, max_price: str):
        ''' Function to set max price
       '''
        self.max_price = max_price

    def set_min_beds_field(self, min_beds: str):
        ''' Function to set min beds
       '''
        self.min_beds = min_beds

    def set_max_beds_field(self, max_beds: str):
        ''' Function to set max beds
       '''
        self.max_beds = max_beds

    def set_min_baths_field(self, min_baths: str):
        ''' Function to set min baths
       '''
        self.min_baths = min_baths

    def print(self):
        ''' Function to print preference object's data. Mostly used while under development to check values are stored. 
       '''
        print (self.location)
        print(self.listing_type)
        print(self.property_type)
        print(self.min_price)
        print(self.max_price)
        print(self.min_beds)
        print(self.max_beds)
        print(self.min_baths)

def gather_preferences() -> Preferences:
    '''A function to gather the prefrences from the user using a pop-up window.
    '''

    # Create Preferences Object
    user_preferences = Preferences()

    # Create Window Object
    preferences_menu = Tk() 
    
    # Initialize tkinter window with dimensions 100x100             
    preferences_menu.geometry('450x300') 
    #preferencesMenu['bg'] = '#ffbf00'
    
    # Add Listing type label
    listing_type = Label(preferences_menu, text = "Listing Type")
    listing_type.place(x = 40, y = 30)
    # Add listing type combo box
    listing_type_options = ttk.Combobox(preferences_menu, width = 20) 
    listing_type_options.place(x = 150, y = 30)
    listing_type_options['values'] = ('sale', 'rent')
    # Saving the option selected
    listing_type_options.bind("<<ComboboxSelected>>", lambda _: user_preferences.set_listing_type_field(listing_type_options.get()))
    
    # Add property label
    property_type = Label(preferences_menu, text = "Property Type")
    property_type.place(x = 40, y = 60)
    # Add property type combo box
    property_type_options = ttk.Combobox(preferences_menu, width = 20) 
    property_type_options.place(x = 150, y = 60)
    property_type_options['values'] = ('house', 'condo', 'townhouse', 'land', 'multifamily')
    # Saving the option selected
    property_type_options.bind("<<ComboboxSelected>>", lambda _: user_preferences.set_property_type_field(property_type_options.get()))
    
    # Add min price label
    min_price_label = Label(preferences_menu, text = "Minimum Price")
    min_price_label.place(x = 40, y = 90)
    # Add min price text field 
    min_price_entry = Entry(preferences_menu, width = 30)
    min_price_entry.place(x = 150,y = 90)
    # Saving data entered into entry field when user leaves the field
    min_price_entry.bind("<Leave>", lambda _: user_preferences.set_min_price_entry_field(min_price_entry.get()))

    # Add max price label
    max_price = Label(preferences_menu, text = "Maximum Price")
    max_price.place(x = 40, y = 120)
    # Add max price entry field
    max_price_entry = Entry(preferences_menu, width = 30)
    max_price_entry.place(x = 150,y = 120)
    # Saving data entered into entry field when user leaves the field
    max_price_entry.bind("<Leave>", lambda _: user_preferences.set_max_price_entry_field(max_price_entry.get()))
    
    # Add min beds label
    min_beds = Label(preferences_menu, text = "Minimum Beds")
    min_beds.place(x = 40, y = 150)
    # Add min beds number scroller
    min_beds_spin_box = Spinbox(preferences_menu, from_= 0, to = 10)
    min_beds_spin_box.place(x = 150, y = 150)
    min_beds_spin_box.bind("<Leave>", lambda _: user_preferences.set_min_beds_field(min_beds_spin_box.get()))
    
    # Add max beds label
    max_beds = Label(preferences_menu, text = "Maximum Beds")
    max_beds.place(x = 40, y = 180)
    # Add max beds number scroller
    max_beds_spin_box = Spinbox(preferences_menu, from_= 0, to = 10)
    max_beds_spin_box.place(x = 150, y = 180)
    max_beds_spin_box.bind("<Leave>", lambda _: user_preferences.set_max_beds_field(max_beds_spin_box.get()))
    
    # Add min baths label
    min_baths = Label(preferences_menu, text = "Minimum Baths").place(x = 40, y = 210)
    # Add min baths number scroller
    min_baths_spin_box = Spinbox(preferences_menu, from_= 0, to = 10, increment = .5)
    min_baths_spin_box.place(x = 150, y = 210)
    min_baths_spin_box.bind("<Leave>", lambda _: user_preferences.set_min_baths_field(min_baths_spin_box.get()))

    #Add Preferences Set Button to close menu
    submit_button = Button(preferences_menu, text = "Submit Preferences", command = preferences_menu.destroy)
    submit_button.place(x = 40, y = 250)
    
    # The Menu is Running!
    preferences_menu.mainloop() 

    # Returning user preferences object
    return user_preferences

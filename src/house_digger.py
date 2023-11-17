#house_digger.py
#----------------------------------
# Created By: Savannah Stephenson
# Created Date: 9/24/2023
#----------------------------------
# Edited By: Savannah Stephenson
# Edit Date: 10/16/2023
# Note: Maybe add a loading screen while the preferences are being added
#----------------------------------
"""This file acts as the runner file for House Digger.
 """ 
#----------------------------------
# 
#Imports
from preference import *
from gather_data import *
import pandas as pd
import tkinter as tk
from pandastable import Table, TableModel


#Gathering User's Preferences
sorting_criteria = gather_preferences()

# Searching according to criteria on redfin.com and printing
#print("redfin.com Listings:")


''' gather the data from the three sites, consolidate into one dataframe, then "drop_duplicates()" '''

# gather data from the three sites

redfin = gather_data_from_redfin(sorting_criteria)
#zillow = gather_data_from_zillow(sorting_criteria).drop_duplicates()
#realtor = gather_data_from_realtor(sorting_criteria).drop_duplicates()

# consolidate into one dataframe
# example df = df.concat(df, zillow)

df = redfin


# drop duplicates
df.drop_duplicates()

# class to create an interactive table of the pandas dataframe (got this from chatGPT btw lol)
class InteractiveTable(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Listings")
        #getting screen width and height of display
        width= self.winfo_screenwidth() 
        height= self.winfo_screenheight()
        #setting tkinter window size
        self.geometry("%dx%d" % (width, height))
        
        # Create a PandasTable Frame
        self.table_frame = tk.Frame(self)
        self.table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create PandasTable
        self.table = Table(self.table_frame, dataframe=df, showtoolbar=True, showstatusbar=True)
        self.table.show()
        
        # Bind a double-click event to the table (optional)
        self.table.bind("<Double-Button-1>", self.on_double_click)
        
    def on_double_click(self, event):
        item = self.table.get_row_clicked(event)
        print("Double clicked on row:", item)


app = InteractiveTable()
app.mainloop()

'''add option to save to csv'''

# print out df (create an interactive table of pandas dataframe ?)
#print(df)
#house_digger.py
#----------------------------------
# Created By: Savannah Stephenson
# Created Date: 9/24/2023
#----------------------------------
# Edited By: 
# Edit Date: 
#----------------------------------
"""This file acts as the runner file for House Digger.
 """ 
#----------------------------------
# 
#Imports
from preference import *
from gather_data import *

#Gathering User's Preferences
sorting_criteria = gather_preferences()

#Searching according to criteria on redfin.com and printing
print("redfin.com Listings:")
print(gather_data_from_redfin(sorting_criteria))


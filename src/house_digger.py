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

#Gathering User's Preferences
sorting_criteria = gather_preferences()

#Searching according to criteria on redfin.com and printing
print("redfin.com Listings:")
print(gather_data_from_redfin(sorting_criteria))

#Searching according to criteria on zillow.com and printing
print("zillow.com Listings:")
print(gather_data_from_zillow(sorting_criteria))


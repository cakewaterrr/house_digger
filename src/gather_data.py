#gather_data.py
#----------------------------------
# Created By: Christian Duff
# Created Date: 10/02/2023
#----------------------------------
# Edited By: 
# Edit Date: 
#----------------------------------
"""This file scrapes data from real estate sites according to passed preferences. 
 """ 
#----------------------------------
# 
#Imports
from bs4 import BeautifulSoup
from preference import *
import requests
import pandas as pd

def gather_data_from_redfin(sort_by: Preferences): 

    # sorting the properties by price (lo-price: low to high, hi-price: high to low)
    sort = 'lo-price' # hardcoding variable for now; need to add to Preferences class

    # number of pages to sift through
    pages = [1,2,3,4,5,6,7,8] # add page 9 (figure out why page 9 i shaving issues)

    # dictionary to hold the attributes of the properties scraped from redfin.com

    homes = {'Address': [],
            'Price': [],
            'Beds': [],
            'Baths': [],
            'Footage': []}
    
    # setting the url for redfin.com 
    if sort_by.listing_type == 'rent':
        url = f'https://www.redfin.com/city/35781/TX/Corpus-Christi/apartments-for-rent/sort={sort},filter/property-type={sort_by.property_type},min-price={sort_by.min_price},max-price={sort_by.max_price},min-beds={sort_by.min_beds},min-baths={sort_by.min_baths},status=active'
    else:
        url = f'https://www.redfin.com/city/35781/TX/Corpus-Christi/filter/sort={sort},property-type={sort_by.property_type},min-price={sort_by.min_price},max-price={sort_by.max_price},min-beds={sort_by.min_beds},max-beds={sort_by.max_beds},min-baths={sort_by.min_baths},status=active'
    
    # loop through and scrape the data from each page
    for page in pages:
        
        if page == 1:
            new_url = url
        else:
            # changing the url based on what page is being scraped 
            new_url = f'{url}/page-{page}' 

        # getting the website from the url
        redfin = requests.get(new_url, headers = {'User-agent': 'Super Bot Power Level Over 9000'})

        # using the soup variable to sift through the html on the website
        soup = BeautifulSoup(redfin.text, 'html.parser')

        # series of conditionals to check what page is being scraped and changing the range of the property numbers
        if(page == 1):
            num = [0, 39]
        if(page == 2):
            num = [40, 80]
        if(page == 3):
            num = [80, 120]
        if(page == 4):
            num = [120, 160]
        if(page == 5):
            num = [160, 200]
        if(page == 6):
            num = [200, 240]
        if(page == 7):
            num = [240, 280]
        if(page == 8):
            num = [280, 320]
        if(page == 9):
            num = [320, 321]

        # looping throught the number of porperties on current page
        for i in range(num[0], num[1]):
            # looking through the html of refin.com, the data is located within these classes and ids
            home_containers = soup.find_all(class_='HomeCardContainer', id=f'MapHomeCard_{i}') 
            stats=home_containers[0].find_all(class_='stats')

            # storing the data for each property into the 'homes' dictionary
            homes['Price'] += [(home_containers[0].find(class_='homecardV2Price').get_text())]
            homes['Address'] += [home_containers[0].find(class_='homeAddressV2').get_text()]
            homes['Beds'] += [stats[0].get_text()]
            homes['Baths'] += [stats[1].get_text()]
            homes['Footage'] += [stats[2].get_text()]

    # converting the dictionary into a pandas dataframe

    properties = pd.DataFrame.from_dict(homes)

    return properties
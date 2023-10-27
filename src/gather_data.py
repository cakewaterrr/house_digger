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
    if sort_by.listing_type == 'rent':
        url = f'https://www.redfin.com/city/35781/TX/Corpus-Christi/apartments-for-rent/filter/property-type={sort_by.property_type[0]},min-price={sort_by.min_price}k,max-price={sort_by.max_price}k,min-beds={sort_by.min_beds},min-baths={sort_by.min_baths}'
    else:
        url = f'https://www.redfin.com/city/35781/TX/Corpus-Christi/filter/property-type={sort_by.property_type[0]},min-price={sort_by.min_price}k,max-price={sort_by.max_price}k,min-beds={sort_by.min_beds},max-beds={sort_by.max_beds}min-baths={sort_by.min_baths}'

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')
    homes = {'Address': [],
            'Price': [],
            'Beds': [],
            'Baths': [],
            'Footage': []}

    # Because there are only 20 viewable houses/"cards" per page...
    for i in range(20):
        home_containers = soup.find_all(class_='HomeCardContainer', id=f'MapHomeCard_{i}')
        stats=home_containers[0].find_all(class_='stats')

        homes['Price'] += [(home_containers[0].find(class_='homecardV2Price').get_text())]
        homes['Address'] += [home_containers[0].find(class_='homeAddressV2').get_text()]
        homes['Beds'] += [stats[0].get_text()]
        homes['Baths'] += [stats[1].get_text()] 
        homes['Footage'] += [stats[2].get_text()]

    properties = pd.DataFrame.from_dict(homes)

    return properties

def gather_data_from_homes(sort_by: Preferences):

    # When searching for homes to rent
    if sort_by.listing_type == 'rent':
            url = f'https://www.homes.com/corpus-christi-tx/homes-for-rent/{sort_by.min_beds}-to-{sort_by.max_beds}-bedroom/?bath-min={sort_by.min_baths}&bath-max=5&price-min={sort_by.min_price}&price-max={sort_by.max_price}'
    # When searching for homes to purchase outright
    '''
    if sort_by.listing_type == 'sale':
            if sort_by.property_type == 'house': # Constructing the URL if the user wants to look for houses for SALE
                url = f'https://www.trulia.com/for_sale/Corpus_Christi,TX/27.23343,28.36317,-97.93012,-96.49091_xy/{sort_by.min_beds}_beds/{sort_by.min_baths}_baths/{sort_by.min_price}-{sort_by.max_price}_price/SINGLE-FAMILY_HOME_type/'
            if sort_by.property_type == 'condo':
                url = f'https://www.trulia.com/for_sale/Corpus_Christi,TX/27.23343,28.36317,-97.93012,-96.49091_xy/{sort_by.min_beds}_beds/{sort_by.min_baths}_baths/{sort_by.min_price}-{sort_by.max_price}_price/APARTMENT,CONDO,COOP_type/'
    '''
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')
    homes = {'Address': [],
            'Price': [],
            'Beds': [],
            'Baths': [],
            'Footage': []}

    for i in range(20):
        home_containers = soup.find_all(class_='placard-container') # Need some sort of ID here?
        stats=home_containers[0].find_all(class_='detailed-info-container')

        homes['Price'] += [(home_containers[0].find(class_='price-container').get_text())]
        homes['Address'] += [home_containers[0].find(class_='property-name').get_text()]
        homes['Beds'] += [stats[0].get_text()]
        homes['Baths'] += [stats[1].get_text()]
        homes['Footage'] += [stats[2].get_text()]

    properties = pd.DataFrame.from_dict(homes)

    return properties
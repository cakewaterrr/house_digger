#gather_data.py
#----------------------------------
# Created By: Christian Duff
# Created Date: 10/02/2023
#----------------------------------
# Edited By: Alicia Mares
# Edit Date: 10/26/23
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

def gather_data_from_realtor(sort_by: Preferences):
    if sort_by.listing_type == 'rent':
        url = f'https://www.realtor.com/apartments/Corpus-Christi_TX/type-{sort_by.property_type[0]}/beds-{sort_by.min_beds}/baths-{sort_by.min_baths}/price-{sort_by.min_price}-{sort_by.max_price}'
    else:
        url = f'https://www.realtor.com/realestateandhomes-search/Corpus-Christi_TX/type-{sort_by.property_type[0]}/beds-{sort_by.min_beds}/baths-{sort_by.min_baths}/price-{sort_by.min_price}-{sort_by.max_price}'

    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')
    homes = {'Address': [],
            'Price': [],
            'Beds': [],
            'Baths': [],
            'Footage': []}

    for i in range(2):
        home_containers = soup.find_all(class_='BasePropertyCard_propertyCardWrap__J0xUj', id=f'MapHomeCard_{i}')
        #stats=home_containers[0].find_all(class_='meta-value')

        #homes['Price'] += [(home_containers[0].find(class_='Pricestyles__StyledPrice-rui__btk3ge-0 bvgLFe card-price').get_text())]
        #homes['Address'] += [home_containers[0].find(class_='card-address truncate-line').get_text()]
        #homes['Beds'] +=   [stats[0].get_text()]
        #homes['Baths'] +=    [stats[1].get_text()]
        #homes['Footage'] +=   [stats[2].get_text()]

    print(home_containers)
    #properties = pd.DataFrame.from_dict(homes)

    #return properties
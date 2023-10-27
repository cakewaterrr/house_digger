#gather_data.py
#----------------------------------
# Created By: Savannah Stephenson
# Created Date: 9/24/2023
#----------------------------------
# Edited By: Christian Duff
# Edit Date: 10/05/2023
#----------------------------------
"""This file uses data scraping methods to pull real estate information from online sites according to the passed preferences. 
 """ 
#----------------------------------
# 
#Imports
from bs4 import BeautifulSoup
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


# EXAMPLE OF FUNCTION RUN BELOW

list_type = 'buy' # 'rent', 'buy'
property_type = 'house' # 'condo', 'townhouse', 'land', 'multifamily' 
min_price = '100k'
max_price = '1M'
min_beds = '1'
max_beds = '4'
min_baths = '1.5'

properties = scraper(list_type, property_type, min_price, max_price, min_beds, max_beds, min_baths)
print(properties)

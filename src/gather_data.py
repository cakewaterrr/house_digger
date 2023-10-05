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

def scraper(list_type, property_type, min_price, max_price, min_beds, max_beds, min_baths):

    property = {'Address': [],
            'Price': [],
            'Beds': [],
            'Baths': [],
            'Footage': []}
    

    # put a while loop here to change URL to go to the next page based on the number of properties per page (looking at redfin)

    if list_type == 'rent':
        #realtor_url = f'https://www.realtor.com/apartments/Corpus-Christi_TX/'
        redfin_url = f'https://www.redfin.com/city/35781/TX/Corpus-Christi/apartments-for-rent/filter/property-type={property_type},min-price={min_price}k,max-price={max_price}k,min-beds={min_beds},min-baths={min_baths}'
    else:
        #realtor_url = f'https://www.realtor.com/realestateandhomes-search/Corpus-Christi_TX/type-single-family-home/beds-2-4/baths-2-3/price-100000-1000000'
        redfin_url = f'https://www.redfin.com/city/35781/TX/Corpus-Christi/filter/property-type={property_type},min-price={min_price}k,max-price={max_price}k,min-beds={min_beds},max-beds={max_beds}min-baths={min_baths}'

    page = requests.get(redfin_url)

    soup = BeautifulSoup(page.text, 'html.parser')

    for i in range(39):
        property_containers = soup.find_all(class_='HomeCardContainer', id=f'MapHomeCard_{i}')
        stats = property_containers[0].find_all(class_='stats')

        property['Price'] += [(property_containers[0].find(class_='homecardV2Price').get_text())]
        property['Address'] += [property_containers[0].find(class_='homeAddressV2').get_text()]
        property['Beds'] += [stats[0].get_text()]
        property['Baths'] += [stats[1].get_text()]
        property['Footage'] += [stats[2].get_text()]



    properties = pd.DataFrame.from_dict(property)

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
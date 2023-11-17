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
from selenium import webdriver
from selenium.webdriver.common.by import By

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

def gather_data_from_zillow(sort_by: Preferences): 
    #zillow uses a captcha to resist scraping so to avoid that use a header
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
              'referer':'https://www.zillow.com/homes/Missoula,-MT_rb/'}
    
    #setting the extension of the URL based on if it's rent or sale
    if sort_by.listing_type == "sale":
        sale_state = "for-sale"
    elif sort_by.listing_type == "rent": 
        sale_state = "rentals"
    
    #making request to save the code of the page provided
    page = requests.get(f'https://www.zillow.com/corpus-christi-tx/{sale_state}', headers=header)

    #process data using bs4 library
    soup = BeautifulSoup(page.text, "lxml")

    #pulling text from page
    address = soup.find_all('address', {'data-test':'property-card-addr'})
    price = soup.find_all('span', {'data-test':'property-card-price'})
    bed_bath_footage = soup.find_all('ul', {'class':'StyledPropertyCardHomeDetailsList-c11n-8-84-3__sc-1xvdaej-0 eYPFID'})

    #formatting the text pulled from page
    adr = []
    pr = []
    beds = [] 
    baths = []
    footage = []
    #formatting addresses into an array
    for result in address: 
        adr.append(result.text)
    #formatting prices into an array
    if sort_by.listing_type == "sale":
        for result in price:
            pr.append(result.text)
    elif sort_by.listing_type == "rent": 
        for result in price: 
            text = result.text 
            head, sep, tail = text.partition('+')
            pr.append(head+sep)
            beds.append(tail)
    #formatting number of beds, baths, and footage
    if sort_by.listing_type == "sale":
        for result in bed_bath_footage:
            #perform some operation on the string to seperate information
            text = result.text
            head, sep, tail = text.partition(',')
            head2, sep2, tail2 = head.partition('s')
            bd = head2+sep2 #operation
            ba = tail2 #operation
            foot = tail
            beds.append(bd)
            baths.append(ba)
            footage.append(foot)
    elif sort_by.listing_type == "rent": 
        for result in address:
            baths.append('Not Listed')
            footage.append('Not Listed')

    #creating homes dictionary
    homes = {'Address': [],
            'Price': [],
            'Beds': [],
            'Baths': [],
            'Footage': []}
    
    #stepping through each array and setting parallel values to home object
    for i in range(len(adr)): 
        homes['Price'] += [pr[i]]
        homes['Address'] += [adr[i]]
        homes['Beds'] += [beds[i]]
        homes['Baths'] += [baths[i]]
        homes['Footage'] += [footage[i]]

    #making data frame using homes
    properties = pd.DataFrame.from_dict(homes)

    #returning the dataframe to display in main
    return properties
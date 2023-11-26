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
    # number of pages to sift through
    pages = [1,2,3,4,5,6,7,8] # add page 9 (figure out why page 9 i shaving issues)

    # dictionary to hold the attributes of the properties scraped from redfin.com

    homes = {'Address': [],
            'Price': [],
            'Beds': [],
            'Baths': [],
            'Footage': [],
            'Source': [] }
    
    # setting the url for redfin.com 
    if sort_by.listing_type == 'rent':
        url = f'https://www.redfin.com/city/35781/TX/Corpus-Christi/apartments-for-rent/filter/property-type={sort_by.property_type[0]},min-price={sort_by.min_price}k,max-price={sort_by.max_price}k,min-beds={sort_by.min_beds},min-baths={sort_by.min_baths}'
    else:
        url = f'https://www.redfin.com/city/35781/TX/Corpus-Christi/filter/property-type={sort_by.property_type[0]},min-price={sort_by.min_price}k,max-price={sort_by.max_price}k,min-beds={sort_by.min_beds},max-beds={sort_by.max_beds}min-baths={sort_by.min_baths}'

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
            homes['Source'] += ['redfin.com']

    # converting the dictionary into a pandas dataframe
    properties = pd.DataFrame.from_dict(homes)

    # deleting things outside of price search parameters for safety
    properties_filtered = properties[(properties['Price'] >= '$' + '{:,}'.format(sort_by.min_price)) & 
                                     (properties['Price'] <= '$' + '{:,}'.format(sort_by.max_price)) ]

    return properties_filtered

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
            head, sep, tail = text.partition(' bds')
            head2, sep2, tail2 = tail.partition(' ba')
            bd = head + ' bed' #operation
            foot = tail2 #operation
            ba = head2 + ' bath'
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
            'Footage': [],
            'Source': []}
    
    #stepping through each array and setting parallel values to home object
    for i in range(len(adr)): 
        homes['Price'] += [pr[i]]
        homes['Address'] += [adr[i]]
        homes['Beds'] += [beds[i]]
        homes['Baths'] += [baths[i]]
        homes['Footage'] += [footage[i]]
        homes['Source'] += ['zillow.com']

    #making data frame using homes
    properties = pd.DataFrame.from_dict(homes)

    #deleting rows that don't meet criteria 
    properties_filtered = properties[(properties['Price'] >= '$' + '{:,}'.format(sort_by.min_price)) & 
                                     (properties['Price'] <= '$' + '{:,}'.format(sort_by.max_price)) & 
                                     (properties['Beds'] >= sort_by.min_beds + ' bed') & 
                                     (properties['Beds'] <= sort_by.max_beds + ' bed') & 
                                     (properties['Baths'] >= sort_by.min_baths + ' bath')]

    #returning the dataframe to display in main
    return properties_filtered

def gather_data_from_trulia(sort_by: Preferences):
    if sort_by.listing_type == 'rent':
        url = f'https://www.trulia.com/for_rent/Corpus_Christi,TX/{sort_by.min_beds}p_beds/{sort_by.min_baths}p_baths/{sort_by.min_price}-{sort_by.max_price}_price/{sort_by.property_type[0]}_type/'
    else:
        url = f'https://www.trulia.com/for_sale/Corpus_Christi,TX/{sort_by.min_beds}p_beds/{sort_by.min_baths}p_baths/{sort_by.min_price}-{sort_by.max_price}_price/{sort_by.property_type[0]}_type/'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')
    homes = {'Address': [],
            'Price': [],
            'Beds': [],
            'Baths': [],
            'Footage': []}

    for i in range(40):
        home_containers = soup.find_all(class_='Grid__CellBox-sc-6b10767f-0 sc-fc01d244-0 fhkpkF kAfNFl', data_testid=f'srp-home-card-{i}')
        rNr=home_containers[0].find_all(class_='Text__TextBase-sc-27a633b1-0-div Text__TextContainerBase-sc-27a633b1-1 cYrgQP gtvmjT') 
        building=home_containers[0].find_all(class_='Text__TextBase-sc-27a633b1-0-div Text__TextContainerBase-sc-27a633b1-1 cYrgQP keSfom')

        homes['Price'] += [(home_containers[0].find(class_='Text__TextBase-sc-27a633b1-0-div Text__TextContainerBase-sc-27a633b1-1 ewcDjf keSfom').get_text())]
        homes['Address'] += [building[1].get_text()]
        homes['Beds'] += [rNr[0].get_text()]
        homes['Baths'] += [rNr[1].get_text()]
        homes['Footage'] += [building[0].get_text()]

    properties = pd.DataFrame.from_dict(homes)

    return properties
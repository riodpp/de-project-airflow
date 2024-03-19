from datetime import datetime, timedelta
from dateutil import parser
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os
import re
import time

# This function extracts the number from a string.
def extract_number(item):
    number = re.findall(r'\d+', item)
    return int(float(number[0])) if number else None

# This function splits the item details string into separate parts and assigns each part to a key in a dictionary.
def item_details_split(item_details):
    item_details = item_details.split(' - ')
    details_dict = {}
    for item in item_details:
        if 'KT' in item:
            details_dict['kt'] = extract_number(item)
        elif 'KM' in item:
            details_dict['km'] = extract_number(item)
        elif 'm2' in item:
            details_dict['luas'] = int(float(item.replace(' m2', '')))
    return details_dict

# This function processes the date string and returns it in the format 'DD/MM/YYYY'.
def process_date(date):
    month_mapping = {'jan': 'jan', 'feb': 'feb', 'mar': 'mar', 'apr': 'apr', 'mei': 'may', 'jun': 'jun', 
                     'jul': 'jul', 'agu': 'aug', 'sep': 'sep', 'okt': 'oct', 'nov': 'nov', 'des': 'dec'}
    date = date.lower().split(' ')
    if 'kemarin' in date[0]:
            return (datetime.now() - timedelta(days=1)).strftime('%Y/%m/%d')
    elif 'hari' in date[1]:
        return (datetime.now() - timedelta(days=int(date[0]))).strftime('%Y/%m/%d')
    elif 'ini' in date[1]:
        return datetime.now().strftime('%Y/%m/%d')
    else:
        date[1] = month_mapping[date[1]]
        date_str = ' '.join(date)
        date_obj = parser.parse(date_str)
        return date_obj.strftime('%Y/%m/%d')

# This function removes the currency and separators from the price string and returns it as an integer.
def clean_price(price):
    return int(price.replace('Rp', '').replace('.', '').replace(' ', ''))

# This function splits the address string into separate parts and assigns each part to a key in a dictionary.
def separate_address(address):
    address = address.split(',')
    address_dict = {}
    if len(address) >= 2:
        address_dict['district'] = address[0].strip()
        city = address[1].strip()
        if 'KAB.' in city or 'KOTA' in city:
            city_parts = city.split(' ')
            city_parts = [city_parts[-1]] + city_parts[:-1]
            city = ' '.join(city_parts)
        address_dict['city'] = city
    else:
        address_dict['district'] = address[0].strip()
        address_dict['city'] = ''
    return address_dict

# load the data to mongodb
def load_data_to_mongodb(data):
    myclient = MongoClient('mongodb://user:password@' + os.environ['MONGODB_HOSTNAME'] + ':27017/')
    # myclient = MongoClient("localhost",27017)
    mydb = myclient["olx_house"]
    mycol = mydb["houses"]
    mycol.insert_many(data)

# Define Options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')  
chrome_options.add_argument('--disable-dev-shm-usage')

# Initialize driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
time.sleep(2)
driver.get('https://www.olx.co.id/dijual-rumah-apartemen_c5158?filter=type_eq_rumah')
driver.find_element('xpath','//a[@data-aut-id="location_Indonesia"]').click()
time.sleep(2)

for i in range(20):
    driver.find_element('xpath','//button[@data-aut-id="btnLoadMore"]').click()

    time.sleep(2)

# Find the ul element for the list of houses
li_elements = driver.find_elements('xpath','//ul[@data-aut-id="itemsList"]/li[@data-aut-id="itemBox"]')

# Create a list of dictionaries to store the house data
houses = []
for li in li_elements:
    house_dict = {}
    price = li.find_element('xpath','.//a/div/span[@data-aut-id="itemPrice"]').text
    itemDetails = li.find_element('xpath','.//a/div/span[@data-aut-id="itemDetails"]').text
    address = li.find_element('xpath','.//a/div/div/span[@data-aut-id="item-location"]').text
    releaseDate = li.find_element('xpath','.//a/div/div/span/span').text
    url = li.find_element('xpath','.//a').get_attribute('href')
    house_dict['price'] = clean_price(price)
    itemDetails = item_details_split(itemDetails)
    house_dict['bedroom'] = itemDetails['kt']
    house_dict['bathroom'] = itemDetails['km']
    house_dict['area'] = itemDetails['luas']
    house_dict['district'] = separate_address(address)['district']
    house_dict['city'] = separate_address(address)['city']
    house_dict['releaseDate'] = process_date(releaseDate)
    house_dict['url'] = url
    house_dict['id'] = url.split('iid-')[1]
    houses.append(house_dict)

driver.quit()

# Load the data to MongoDB
load_data_to_mongodb(houses)
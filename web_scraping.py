# import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re

# take product name from user
s = input("Enter product name (example: mi smartphone): ")

# first part of url for amazon
url1 = "https://www.amazon.in/s?k="

# creating the complete url
for i in s.split():
    url1 += i + "+"
    
if url1[-1] == "+":
    URL = url1[:len(url1)-1]
else:
    URL = url1

print(URL)

# extracting the html informarion
while True:
    try:
        # user-agent        
        HEADERS = ({"User-Agent":
                   "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
                    "Accept-Language": "en-US, en;q=0.5"})
        r = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(r.content, "html5lib")
        break
    except:
        # a random time delay before next request (regular users won't be requesting urls at constant interval)
        time.sleep(random.randint(10,20))
        pass

# array to store the product details
products = []

# extract name and price of the product
for row in soup.findAll("div", attrs = {"data-component-type" : "s-search-result"}):
    
    # for clearing the html tags
    cleanr = re.compile('<.*?>')
    # dictionary to store the product name and details
    product = {} 
    
    name = str(row.find("span", attrs={"class":"a-size-medium a-color-base a-text-normal"}))
    product["name"] = re.sub(cleanr, '', name)
    price = str(row.find("span", attrs={"class":"a-price-whole"}))
    product["price"] = re.sub(cleanr, '', price)
    
    products.append(product)

# saving the scraped details to csv    
df = pd.DataFrame(products)
fname = s+".csv"
df.to_csv(fname)
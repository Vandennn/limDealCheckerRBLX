#import selenium
#from selenium import webdriver
from bs4 import BeautifulSoup
#from selenium.webdriver.common.by import By
import json
#from selenium.common.exceptions import NoSuchElementException
#from selenium.common.exceptions import StaleElementReferenceException
import requests
import re


#CONFIG

sortBy = "Most Recent"
hideDealsBelow = 35
projections = "Hide"
dealCalc = "value"
url = "https://www.rolimons.com/deals"

proxies = {
    'SOCKS4': '23.94.47.24:32129',
    'SOCKS4': '66.78.54.93:20000'
}
#--------------------------------------

#driver = webdriver.Chrome()
#driver.get(url)

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

#check if limited


#print(soup)
varFind = soup.find_all('script')
bestDeal = 0
bDName = ""
bDPrice = 0
bDID = 0
for i in varFind:
    varStr = i.string
    if varStr and 'var item_activity' in varStr:
        pattern = r'var item_activity = ({.*?});'
        match = re.search(pattern, varStr)
        if match:
            item_activity_json = match.group(1)
            item_activity_dict = json.loads(item_activity_json)
            first_key, first_value = next(iter(item_activity_dict.items()))
            for x in item_activity_dict:
                temp = item_activity_dict[x]

                if temp[3] == 0 or temp[2] == 0:
                    deal = None
                else:
                    if(float(1 - (temp[2]/temp[3]))) < 0:
                        deal = None
                    else:
                        deal = float(1 - (temp[2]/temp[3])) * 100
                        deal = int(deal)
                        if deal > bestDeal:
                            bestDeal = deal
                            bDName = temp[0]
                            bDPrice = temp[2]
                            bDID = x
                #response = requests.get("https://www.rolimons.com/item/" + x)
                #soup = BeautifulSoup(response.content, "html.parser")
                #projFind = soup.find(class_="text-nowrap mr-2")
                #print(projFind)



                print("Item Link:", "https://www.roblox.com/catalog/" + x, "\n", 
                "Item Name:", temp[0], "\n",
                "Item Price:", temp[2], "\n",
                "Item RAP:", temp[3], "\n",
                "Item Deal:", deal)
print("Best Deal:", bestDeal, "\n"
    "Best Item Name:", bDName, "\n",
    "Best Item Price:", bDPrice, "\n",
    "Item Link:", "https://www.roblox.com/catalog/" + bDID)
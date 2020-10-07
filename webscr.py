from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup, NavigableString
import requests
import os
import page_data


source = requests.get(page_data.auctions_fill).text

soup = BeautifulSoup(source, 'lxml')
for auction in soup.find_all('div', class_='auctionObjectRight'):
    leftSide = auction.find('span', {"class":"leftSide"})
    inner_text = [element for element in leftSide if isinstance(element, NavigableString)]
    text = inner_text[0].replace("\t", "")
    text = text.replace("\n", "")
    print(text)

    cur_price = auction.find('p', {"class":"startPrice"}).text
    print(cur_price)

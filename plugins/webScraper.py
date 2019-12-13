# coding: UTF-8

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class AmazonScrape():

    def __init__(self,_url):
        self.html = requests.get(_url)
        self.soup = BeautifulSoup(self.html.text, features="lxml")

    def GetBrand(self):
        selected_html = self.soup.select('#bylineInfo')
        brand = selected_html[0].text
        return brand

    def GetName(self):
        selected_html = self.soup.select('#productTitle')
        name = selected_html[0].text
        name = name.replace(' ', '')
        name = name.replace('\n', '')
        return name

    def GetPrice(self):
        selected_html = self.soup.select('#priceblock_ourprice')
        price = selected_html[0].text
        price = price.replace("￥","") #￥先頭のマークを消す
        price = price.replace(",","")
        return int(price)

class  MonotaroScrape():
    def __init__ (self, _url):
        options = webdriver.chrome.options.Options()
        #options.add_argument('--headless') #ヘッドレスだと動かない

        self.browser = webdriver.Chrome("/Users/masato/Desktop/chromedriver",chrome_options=options)
        #self.browser = webdriver.Chrome("/Users/masato/Desktop/chromedriver")
        self.browser.get(_url)
        self.browser.implicitly_wait(1)

        self.html = self.browser.page_source
        self.soup = BeautifulSoup(self.html, "html.parser")

    def quit(self):
        self.browser.quit()
        
    def GetBrand(self):
        brand = self.soup.find("span", class_="itd_brand")
        #print(brand)
        brand = brand.get_text().replace('\n','')
        return brand

    def GetName(self):
        name = self.soup.find("span", class_="item")
        #print(name)
        name = name.get_text()
        return name

    def GetPrice(self):
        item_info = self.soup.find("dl", class_="itd_info_dl")

        item_info = item_info.find_all("dd")
        price = item_info[len(item_info)-1].get_text().replace("\n","")

        price = price.replace("￥","") #￥先頭のマークを消す
        price = price.replace(",","") #カンマ消す
        return int(price)
    
    def GetProductNumber(self):
        item_info = self.soup.find("dl", class_="itd_info_dl")
        item_info = item_info.find_all("dd")
        productNum = item_info[0].get_text().replace("\n","")

        return productNum


# coding: UTF-8

import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time

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
        #例外処理

        self.browser = webdriver.PhantomJS("/Users/masato/node_modules/phantomjs/lib/phantom/bin/phantomjs")#ブラウザを操作するオブジェクトを生成
        self.browser.get(_url)

        self.html = self.browser.page_source
        self.soup = BeautifulSoup(self.html, features="lxml")
        

    def GetBrand(self):
        brand = self.soup.find("span", class_="itd_brand")
        print(brand)
        brand = brand.get_text().replace('\n','')
        return brand

    def GetName(self):
        name = self.soup.find("span", class_="item")
        name = name.get_text()
        return name

    def GetPrice(self):
        item_info = self.soup.find("div",class_="itd_base_info")
        print(item_info)
        #for item in item_info:
        #    print(item.text)
        #item_info = item_info.find_all("dd")
        #price = item_info[-1].get_text().replace("\n","")
        #price = price.replace("￥","") #￥先頭のマークを消す
        #price = price.replace(",","")
        price = "1"
        return int(price)

monotaro = MonotaroScrape("https://www.monotaro.com/p/3260/6375/")
time.sleep(2)
print(monotaro.GetName())
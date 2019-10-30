# coding: UTF-8

import requests
from bs4 import BeautifulSoup

class AmazonScrape():

    def __init__(self,_url):
        self.html = requests.get(_url)
        self.soup = BeautifulSoup(self.html.text, features="lxml")

    def GetMaker(self):
        selected_html = self.soup.select('#bylineInfo')
        maker = selected_html[0].text
        return maker

    def GetTitle(self):
        selected_html = self.soup.select('#productTitle')
        title = selected_html[0].text
        title = title.replace(' ', '')
        title = title.replace('\n', '')
        return title

    def GetPrice(self):
        selected_html = self.soup.select('#priceblock_ourprice')
        price = selected_html[0].text
        price = price.replace("￥","") #￥先頭のマークを消す
        price = price.replace(",","")
        return int(price)
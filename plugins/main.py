# coding: UTF-8

from slackbot.bot import respond_to
import plugins.webScraper as ws

@respond_to("(.*)")
def order(message, arg1):
    orderdata = str(message.body['text'])
    if(' ' in orderdata):
        orderdata = orderdata.split(' ')
        print(len(orderdata))
        #orderデータが3つより多い場合フォーマットが異なるのでエラーを返す
        if(3 <= len(orderdata)):
            InputFormatError(message)

    else:
        orderdata = orderdata.replace("<","")
        orderdata = orderdata.replace(">","")
        result = OrderFormat(orderdata,"1")
        message.reply(result)

def OrderFormat(url,num):
    maker,title,price = GetInfomation(url)
    if(maker != -1):
        formatTex = "・メーカ名:"+maker+"\n"
        formatTex = formatTex + "・製品名:" + title + "\n"
        formatTex = formatTex + "・単価:￥" + "{:,}".format(price)+ "\n"
        formatTex = formatTex + "・個数:" + num + "\n"
        formatTex = formatTex + "・合計価格:￥" + "{:,}".format(price*int(num)) + "\n"
        if("amazon.co.jp" in url):
            formatTex = formatTex + "・販売店:Amazon \n"
        elif("monotaro.com" in url):
            formatTex = formatTex + "・販売店:モノタロウ \n"
        else:
            formatTex = formatTex + "・販売店:Unknown \n"

        formatTex = formatTex + "・参考URL:" + url + "\n"

        return formatTex

    else:
        return "Amazon or モノタロウのURLのみ使用出来ます"
    


def GetInfomation(url):
    if("amazon.co.jp" in url):
        scraper = ws.AmazonScrape(url)
    else:
        return -1,-1,-1

    maker = scraper.GetMaker()
    title = scraper.GetTitle()
    price = scraper.GetPrice()

    return maker,title,price

def InputFormatError(message):
    message.reply("以下のフォーマットで送信してください\n 1. :amazon: or :monotarou:のURLのみ \n 2. :amazon: or :monotarou:のURL (スペース) 発注数")
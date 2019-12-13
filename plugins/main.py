# coding: UTF-8

from slackbot.bot import respond_to
import plugins.webScraper as ws

@respond_to("(.*)")
def order(message, arg1):
    orderdata = str(message.body['text'])
    if(' ' in orderdata):
        orderdata = orderdata.split(' ')
        #orderデータが3つより多い場合フォーマットが異なるのでエラーを返す
        if(3 <= len(orderdata)):
            InputFormatError(message)
        else:
            orderdata[0] = orderdata[0].replace("<","")
            orderdata[0] = orderdata[0].replace(">","")
            result = OrderFormat(orderdata[0],orderdata[1])
            message.reply(result)

    else:
        orderdata = orderdata.replace("<","")
        orderdata = orderdata.replace(">","")
        result = OrderFormat(orderdata,"1")
        message.reply(result)

def OrderFormat(url,num):
    if("amazon.co.jp" in url):
        maker,name,price = GetInformation(url)
    elif ("monotaro.com" in url):
        maker, name, price, productNum = GetInformation(url)
    else:
        maker, name, price = GetInformation(url)

    if(maker != -1):
        formatTex = "・メーカ名:"+maker+"\n"
        formatTex = formatTex + "・製品名:" + name + "\n"
        if("monotaro.com" in url):
            formatTex = formatTex + "・注文コード:"+productNum+"\n"
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
    


def GetInformation(url):
    if("amazon.co.jp" in url):
        scraper = ws.AmazonScrape(url)
    elif("monotaro.com" in url):
        scraper = ws.MonotaroScrape(url)
    else:
        return -1,-1,-1

    maker = scraper.GetBrand()
    name = scraper.GetName()
    price = scraper.GetPrice()
    if("monotaro.com" in url):
        productNum = scraper.GetProductNumber()
        scraper.quit()
        return maker, name, price, productNum
    elif("amazon.co.jp" in url):
        return maker, name, price
    
    return -1, -1, -1

def InputFormatError(message):
    message.reply("以下のフォーマットで送信してください\n 1. Amazon:amazon: or モノタロウ:monotarou:のURLのみ \n 2. :amazon: or :monotarou:のURL (スペース) 発注数")
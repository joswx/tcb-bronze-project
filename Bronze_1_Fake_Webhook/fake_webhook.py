import requests
import json
import time
import sys
import os
sys.path.append(os.path.dirname(__file__))
from builder import * 

#input webhook url here
WEBHOOK_URL = ''

def runner():
    """
    initialize the input process to allow user to customize product information, use default when input product name is empty, returns a populated dict to send as data

    :return: dict
    """
    print("Webhook 模拟器启动，目前支持推送 Balkobot 和 Cybersole 的webhook")
    botName = input("请输入需要使用的Bot 全称: e.g Balkobot/Cybersole: \n")
    while (botName != "Balkobot" and botName != "Cybersole"):
        print(botName)
        print("你输入的bot 名称有误")
        botName = input("请输入需要使用的Bot 全称: e.g Balkobot/Cybersole: ")
    productData = {}
    productData['Product'] = input("请输入产品名称, 如果想调用后台已有产品信息，请直接回车: ")
    if not productData['Product']:
        return populating_template(template=template_builder(botName = botName))
    try:
        productData["Size"] = input("请输入尺码 (US): ") or "N/A"
        productData["Picture_url"] = input("请输入产品图片url，如无请回车: ")
        productData["Store"] = input("请输入商店名，如无请回车: ") or "N/A"
        productData["Profile"] = input("请输入Profile名称，如无请回车: ") or "N/A"
        productData["Order"] = input("请输入Order Number，如无请回车: ") or "N/A"
        productData["Proxy List"] = input("请输入Proxy List名称，如无请回车: ") or "N/A"
        productData["Mode"] = input("请输入Mode, 如无请回车: ") or "N/A"
        productData["Delay"] = input("请输入Task Delay, 如无请回车: ") or "N/A"
        productData["Tasks"] = input("请输入Task数量, 如无请回车: ") or "N/A" 
    except:
        print("输入信息有误兄弟")
        raise(sys.exit(e))
    return populating_template(template=template_builder(botName=botName), productData = productData)

def webhook_sender(url=WEBHOOK_URL):
    """
    Webhook sender using default webhook url and data populated from runner, post the request to the webhook link

    :param url: webhook url
    :type url: str
    """
    data = runner()
    print(json.dumps(data))
    try:
        r = requests.post(url,json=data)
        print(r)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

if __name__ == '__main__':
    while True:
        webhook_sender()
        print("10秒后重启")
        time.sleep(10)
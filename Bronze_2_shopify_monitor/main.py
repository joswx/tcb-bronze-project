import requests
import json
import sys
import os
sys.path.append(os.path.dirname(__file__))
from monitor import *
import time

WEBHOOK_URL = 'https://discordapp.com/api/webhooks/698806611099254831/buR4_-uKP-mjPTz8ieGJwf7t0Yh7DXXLKn_FWGZudbdpXyYKZnW07L03BnfXCb7T8VR6'
url = "https://undefeated.com/collections/all/products/adidas-x-undefeated-ultraboost-blkwhi"



if __name__ == '__main__':
    webhook_url = input("请输入你的webhook url: ")
    product_url = input("请输入你想监控的Shopify 商品地址(去除?variants=的后缀): ")
    while True:
        r = webhook_sender(webhook_url=webhook_url, product_url=product_url)
        if not r:
            print("监控失败，请检查console log")
        print("正在监控: {}".format(product_url))
        time.sleep(20)

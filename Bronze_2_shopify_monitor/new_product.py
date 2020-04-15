import requests
import json
import os
from os import path
import time
from monitor import *

URL = "https://undefeated.com/products"
PROJECT_ROOT_DIR = '.'
RESOURCE_DIR = os.path.join(PROJECT_ROOT_DIR, 'resource')
WEBHOOK_URL = 'https://discordapp.com/api/webhooks/698806611099254831/buR4_-uKP-mjPTz8ieGJwf7t0Yh7DXXLKn_FWGZudbdpXyYKZnW07L03BnfXCb7T8VR6'

def get_latest_products(url=URL):
    data = fetch_json(url=URL)
    res = {}
    product_list = []
    if data:
        for product in data['products']:
            product_list.append(product['id'])
        res['products'] = product_list
        latestFile_path = os.path.join(RESOURCE_DIR, 'latest_products.json')
        if path.exists(latestFile_path):
            os.rename(latestFile_path,os.path.join(RESOURCE_DIR, 'prev_products.json'))
        with open('./resource/latest_products.json','w') as file:
            json.dump(res,file)
        file.close()

def get_new_products_id(latest='latest_products.json', prev = 'prev_products.json'):
    try:
        with open(os.path.join(RESOURCE_DIR,latest)) as file:
            latest_data = json.load(file)['products']
        file.close()
        with open(os.path.join(RESOURCE_DIR, prev)) as file:
            prev_data = json.load(file)['products']
        file.close()
        return [x for x in latest_data if x not in prev_data]
    except IOError:
        print("latest product list not found!")
        return 
        

def new_product_processor(ids=get_new_products_id(), data=fetch_json(url=URL)):
    product_list = []
    if ids:
        for product in data['products']:
            if product['id'] in ids:
                product_info = {}
                product_info['title'] = product['title']
                product_info['image'] = product['images'][0]['src']
                variants = []
                for variant in product['variants']:
                    tmp = {}
                    tmp['Size'] = variant['option2']
                    tmp['Variant'] = variant['id']
                    variants.append(tmp)
                product_info['variants'] = variants
                product_list.append(product_info)
        return product_list
    else:
        return


def webhook_builder(data=new_product_processor()):
    webhooks = []
    if data:
        for item in data:
            template = template_loader(template_file='webhook_template.json')
            template['embeds'][0]['title'] = item['title']
            template['embeds'][0]['author']['name'] = 'Undefeated'
            template['embeds'][0]['author']['url'] = "https://undefeated.com"
            template['embeds'][0]['thumbnail']['url'] = item['image']
            numVariants = len(item['variants'])
            fields = []
            if numVariants > 0:
                halfSize = numVariants / 2 + 1
                i = 0
                message = ""
                while (i < halfSize):
                    partial = "[{}]({}/cart/{}:1) | [{}]({}/cart/{}:1) \n".format(
                        item['variants'][i]['Size'], URL, item['variants'][i]['Variant'], item['variants'][i+1]['Size'], URL, item['variants'][i+1]['Variant'])
                    message += partial
                    i += 2
                tmp = {}
                tmp['name'] = 'ATC'
                tmp['value'] = message
                tmp['inline'] = True
                fields.append(tmp)
                message = ""
                while (i < numVariants):
                    if i < len(item['variants']) - 1:
                        partial = "[{}]({}/cart/{}:1) | [{}]({}/cart/{}:1)\n".format(
                            item['variants'][i]['Size'], URL, item['variants'][i]['Variant'], item['variants'][i+1]['Size'], URL, item['variants'][i+1]['Variant'])
                    else:
                        partial = "[{}]({}/cart/{}:1) | \n".format(item['variants'][i]
                                                                   ['Size'], URL, item['variants'][i]['Variant'])
                    i += 2
                    message += partial
                tmp = {}
                tmp['name'] = 'ATC'
                tmp['value'] = message
                tmp['inline'] = True
                fields.append(tmp)
            template["embeds"][0]["fields"] = fields
            webhooks.append(template)
        return webhooks

if __name__ == '__main__':
    #get_latest_products()
    print("Currently monitoring Undefeated.com")
    webhooks = webhook_builder()
    if webhooks:
        for webhook in webhooks:
            webhook_sender(data=webhook,product_url=None,webhook_url = WEBHOOK_URL)
    time.sleep(60)


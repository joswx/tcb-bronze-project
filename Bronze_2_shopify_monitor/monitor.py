import requests
import json
import os

#default url
URL = 'https://undefeated.com/collections/all/products/air-zoom-spiridon-cage-2-ltsmokegrey-metallicsilver'
WEBHOOK_URL = ''
PROJECT_ROOT_DIR = "."
RESOURCE_DIR = os.path.join(PROJECT_ROOT_DIR,"resource")

def fetch_json(url = URL):
    """
    :fetch json data from input url

    :param url: input url to fetch for json data
    :type url: str
    :return dict
    """
    url = url + '.json'
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = json.loads(r.text)
            if 'product' in data:
                data['product']['url'] = url.split(".json")[0]
                data['product']['homepage_url'] = url.split("/collections/")[0]
            return data
        else:
            print('Error fetching url with status code {}'.format(r.status_code)) # can be logger
            return
    except requests.exceptions.RequestException as e:
        print("Error getting response from url with {}".format(e)) # can be logger
        return

def template_loader(template_file = "product_template.json"):
    """
    :load predefined json template

    :param template_file: tempalte file name to load
    :type templatE_file: str
    :return: dict
    """
    templatePath = os.path.join(RESOURCE_DIR,template_file)
    try:
        with open(templatePath) as file:
            template = json.load(file)
            return template
    except: 
        print("Error loading template")
        return

def processor(template= template_loader(),product_url = URL): 
    """
    :populate template with loaded data

    :param template: predefined template
    :type template: dict
    :param product_url: product url to load data
    :type product_url: str
    :return: dict
    """
    data = fetch_json(url = product_url)
    if not template or not data:
        print("error getting resources")
        return
    res = {}
    try:
        for key in template:
            keyPath = template[key]["path"].split("@")
            tmp = data
            for i in range(len(keyPath)):
                if isinstance(tmp, list):
                    index = int(keyPath[i])
                    tmp = tmp[index]
                else:
                    tmp = tmp[keyPath[i]]
            if not template[key]["list"]:
                res[key] = tmp
            else:
                nested = []
                for item in tmp:
                    attributes = template[key]["attributes"]
                    tmp_dict = {}
                    for attribute in attributes:
                        if attribute == "option2":
                            tmp_dict['Size'] = item[attribute]
                        else:
                            tmp_dict[attribute] = item[attribute]
                    nested.append(tmp_dict)
                res[key] = nested
        return res
    except:
        print("Error processing data")
        return


def request_builder(product_url = URL,webhook_template=template_loader(template_file="webhook_template.json")):
    """
    :build request body with loaded data and template

    :param product_url: product url to load the data 
    :type product_url: str
    :param webhook_template: webhook tempalte file name to load
    :type webhook_template: str
    :param template_file: template file name to load
    :type template_file: str
    :return dict
    """
    data = processor(product_url=product_url)
    if not data:
        print("Error getting product data")
        return
    if not webhook_template:
        print("Error getting wehbook template")
        return
    webhook_template["embeds"][0]['title'] = data['title']
    webhook_template["embeds"][0]['author']["name"] = data['homepage_url'].split("//")[1]
    webhook_template["embeds"][0]['author']["url"] = data['homepage_url']
    webhook_template["embeds"][0]['url'] = data['url']
    webhook_template["embeds"][0]['thumbnail']['url'] = data['image']
    fields = []
    fixed_attributes = ['Price','Stock']
    for i in range(len(fixed_attributes)):
        tmp = {}
        tmp['name'] = fixed_attributes[i]
        if fixed_attributes[i].lower() in data:
            tmp['value'] = data[fixed_attributes[i].lower()]
        else:
            tmp['value'] = 'N/A'
        tmp['inline'] = False
        fields.append(tmp)
    numVariants  = len(data['variants'])
    if numVariants > 0:
        halfSize = numVariants / 2 + 1
        i = 0
        message = ""
        while (i < halfSize):
            partial = "[{}]({}/cart/{}:1) | [{}]({}/cart/{}:1) \n".format(
                data['variants'][i]['Size'], data['homepage_url'], data['variants'][i]['id'], data['variants'][i+1]['Size'], data['homepage_url'], data['variants'][i+1]['id'])
            message += partial
            i += 2
        tmp = {}
        tmp['name'] = 'ATC'
        tmp['value'] = message
        tmp['inline'] = True
        fields.append(tmp)
        message = ""
        while (i < numVariants):
            if i < len(data['variants']) - 1:
                partial = "[{}]({}/cart/{}:1) | [{}]({}/cart/{}:1)\n".format(
                data['variants'][i]['Size'], data['homepage_url'], data['variants'][i]['id'], data['variants'][i+1]['Size'], data['homepage_url'], data['variants'][i+1]['id'])
            else:
                partial = "[{}]({}/cart/{}:1) | \n".format(data['variants'][i]
                                                    ['Size'], data['homepage_url'], data['variants'][i]['id'])
            i += 2
            message += partial
        tmp = {}
        tmp['name'] = 'ATC'
        tmp['value'] = message
        tmp['inline'] = True
        fields.append(tmp)
    webhook_template["embeds"][0]["fields"] = fields
    return webhook_template

def webhook_sender(webhook_url = WEBHOOK_URL, product_url = URL, data = None):
    """
    :send webhook with populated body

    :param webhook_url: webhook url to send to
    :type webhook_url: str
    :param product_url: product url to load
    :type product_url: str
    :param data: product data
    :type data: dict
    """
    if not data:
        data = request_builder(product_url = product_url);
    if data:
        try:
            r = requests.post(webhook_url,json = data)
            if r.status_code > 400:
                print("Status Error: {}".format(r.status_code))
                return
            return r
        except requests.exceptions.RequestException as e:
            print("Error getting response from url with {}".format(e))  # can be logger
            return
    else:
        print("Error fetching and processing product data")
        return
    

    
    
    
                



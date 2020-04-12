import json
import os
import random

PROJECT_HOME_DIR = "."
DATA_DIR = os.path.join(PROJECT_HOME_DIR, "data")


def json_loader(fileName):
    """
    loading json files from default folder

    :param fileName: input json file to load
    :type fileName: str
    :return: dict
    """
    file_dir = os.path.join(DATA_DIR, fileName)
    with open(file_dir) as json_file:
        data = json.load(json_file)
    return data

def template_builder(fileName = "bots.json", botName="Balkobot"):
    """
    build template based on default bot config and bot name

    :param fileName: input bot template to load
    :type fileName: str
    :param botName: input bot name to use
    :type botName: str
    :return: dict
    """
    template = json_loader(fileName)[botName]
    return template

def populating_template(template=template_builder(), productData = None,productFile = "product.json"):
    """
    populate existing tempalte with data, use default product files when input product data is missing

    :param template: dict built from template builder
    :type template: dict
    :param productData: input dict that contains product data
    :type productData: dict
    :param productFile: default product data file name
    :type productFile: str
    :return: dict
    """
    if not productData:
        productData = random.choice(json_loader(productFile)['products'])
    containsProductField = False
    for i in range(len(template["embeds"][0]["fields"])):
        key = template["embeds"][0]["fields"][i]["name"]
        if key == "Product":
            containsProductField = True
        if key in productData:
            template["embeds"][0]["fields"][i]["value"] = productData[key]
    if not containsProductField:
        template["embeds"][0]["description"] = productData["Product"]
    template["embeds"][0]['url'] = productData['url']
    template["embeds"][0]["thumbnail"]['url'] = productData["Picture_url"]
    return template

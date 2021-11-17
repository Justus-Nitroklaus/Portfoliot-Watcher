import urllib
import json
import shutil
from bs4 import BeautifulSoup
from scripts.functions import readJson
import requests



def safeAllIcons():
    investments = readJson('investments.json')
    for i in range(len(investments)):
        coin = investments[i]["name"]
        try:
            f = open('icons/{}.png'.format(coin))
        except IOError:
            safeIcon(coin)
        finally:
            f.close()


# Safe Icon of a specific coin in icons directory
def safeIcon(coinName):
    url =''.join(['https://coinmarketcap.com/currencies/', coinName])
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        image_url = soup.find_all('img')[1].get('src')
        image = requests.get(image_url, stream=True)
        if image.status_code == 200:
            image.raw.decode_content = True
            with open('icons/{}.png'.format(coinName), 'wb') as file:
                shutil.copyfileobj(image.raw, file)
    except IndexError:
        print("Die angegebene URL \"https://coinmarketcap.com/currencies/{}\"".format(coinName) + " konnte nicht gefunden werden")
import requests 
import rumps
from scripts.jsonmethods import *
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from currency_converter import CurrencyConverter 
from forex_python.converter import CurrencyRates

def getSellingStats(sells):
    averageSellingPrice = amountSold = profit = 0
    for i in range(len(sells)):
        amountSold += float(sells[i]["amountSold"])
        profit += (float(sells[i]["amountSold"]) * float(sells[i]["price"]))
    return [profit, amountSold]

# Iterates over every coin in investments.json and calls safeIcon() on that coin
def getSingleValues(coin):
    values = readJson('currentValues.json')
    for i in range(len(values) - 1):
        if values[i]["1. Coin"] == coin:
            coinValue = values[i]
    return coinValue["6. Aktueller Wert"] + " | " + coinValue["3. Investiert"] + " | " + coinValue["8. Prozentsatz"]

def getNewValues():
    emptyJsonFile('currentValues.json')
    storeOutputJsonData(json.dumps(getCurrentInvestmentStats(), indent = 4, sort_keys = True))
    data = readJson('currentValues.json')
    i = len(data) - 1
    return data[i]["1. Gesamtwert"] + " | " + data[i]["2. Gesamt investiert"] + " | " + data[i]["4. Prozentsatz"]


def getCoinNames():
    coinNames = []
    investments = readJson('investments.json')
    for i in range(len(investments)):
        coinNames.append(investments[i]["name"])
    return coinNames

#Get price of a coin in EUR
def getCoinPrice(coinTicker, coinName):
    url = 'https://rest.coinapi.io/v1/exchangerate/{}/EUR'.format(coinTicker)
    headers = {'X-CoinAPI-Key': '65EFE974-924B-4EDB-97A5-F423E1632FF3'}
    response = requests.get(url, headers=headers)
    try:
        return response.json()["rate"]
    except:
        c = CurrencyConverter()
        url = ''.join(['https://coinmarketcap.com/currencies/', coinName])
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
        else: 
            return "Error"
        string = soup.find_all('div', class_='priceValue')
        if len(string) == 0:
            print("Fehler in Coin:" + coinName)
        price = string[0].text.replace('$', '').replace(',', '')
        return c.convert(float(price),'USD', 'EUR') 

#Go through all investments and calculate the current Value of the Portfolio
def getCurrentInvestmentStats():
    investments = readJson('investments.json')
    currentStats = []
    overallValue = overallProfit = overallInvested = 0
    for i in range(len(investments)):
        sells = []
        name = investments[i]["name"]    
        currentPrice = getCoinPrice(investments[i]["ticker"], name)
        invested = averageCost = coinAmount = amountSold = averagePrice = earnings = profit = coinsSold = 0
        for j in range(len(investments[i]["buys"])):
            coinAmount += float(investments[i]["buys"][j]["amountBought"])
            invested += float(investments[i]["buys"][j]["spent"])
        averageCost = invested / coinAmount
        if investments[i]["sold"] == "True":
            sells = getSellingStats(investments[i]["sells"])
            profit = sells[0]
            coinsSold = sells[1]
        coinValue = currentPrice * (coinAmount - coinsSold)
        overallValue += coinValue + profit
        overallInvested += invested
        overallProfit += profit 
        dict = {
            "1. Coin": name,
            "2. Kaufpreis": "{:.2f}".format(averageCost) + " EUR",
            "3. Investiert": "{:.2f}".format(invested) + " EUR",
            "4. Anzahl Coins": "{:.2f}".format(coinAmount - coinsSold),
            "5. Aktueller Preis": "{:.2f}".format(currentPrice) + " EUR",
            "6. Aktueller Wert": "{:.2f}".format(coinValue + profit) + " EUR",
            "7. Gewinn/Verlust": "{:.2f}".format(coinValue - invested + profit) + " EUR",
            "8. Prozentsatz": "{:.2f}".format(((coinValue + profit) / invested) * 100) + "%"
        }
        currentStats.append(dict)
    dict = {
        "1. Gesamtwert": "{:.2f}".format(overallValue) + " EUR",
        "2. Gesamt investiert": "{:.2f}".format(overallInvested) + " EUR",
        "3. Gewinn/Verlust": "{:.2f}".format(overallValue - overallInvested) + " EUR",
        "4. Prozentsatz": "{:.2f}".format(((overallValue + profit) / overallInvested) * 100) + "%",
        "5. Gezogener Profit": "{:.2f}".format(overallProfit) + " EUR"
    }
    currentStats.append(dict)
    return currentStats

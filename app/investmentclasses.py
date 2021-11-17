from scripts.jsonmethods import readJson

class investment(object):
    def __init__(self, name, amountBought, moneyInvested, currentPrice):
        self.name = name
        self.amountBought = amountBought
        self.moneyInvested = moneyInvested
        self.currentPrice = currentPrice
        self.averageBuyIn = self.moneyInvested / self.amountBought
        self.profit = self.currentPrice * self.amountBought - self.moneyInvested
        self.percentage = self.profit / self.moneyInvested

def createInvestmentList():
    newInvestmentList = []
    data = readJson('currentValues.json')
    for i in range(len(data) - 1):
        newInvestment = investment(data[i]["1. Coin"], float(data[i]["4. Anzahl Coins"]), float(data[i]["3. Investiert"][:-3]), float(data[i]["5. Aktueller Preis"][:-3]))
        newInvestmentList.append(newInvestment)
    return newInvestmentList
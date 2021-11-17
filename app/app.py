import rumps 
#import subprocess
#import shlex
#import time
import os
from scripts.functions import *
from scripts.jsonmethods import *
from app.investmentclasses import *

class WalletWatcherApp(object):

    def __init__(self):
        self.config = {
            "app_name": "WalletWatcher",
            "iterator": 0
        }
        self.investmentList = createInvestmentList()
        self.app = rumps.App("WalletWatcher", "WalletWatcher")
        self.setUpMenu()

    def setUpMenu(self):
        self.app.title = getNewValues()
        self.reloadButton = rumps.MenuItem(title="Reload Value", callback=self.printNewValues, icon='icons/mainicon.png')
        self.show_all_Button = rumps.MenuItem(title="Show all", callback=self.showAll, icon='icons/mainicon.png')
        self.coins = []
        self.app.menu = [
            self.reloadButton,
            self.show_all_Button,
            None]   
        for i in range(len(self.investmentList)):
            title = self.investmentList[i].name
            callback = lambda _, j=title: self.getStats(_ , j)
            icon = 'icons/{}.png'.format(title)
            self.coins.append(rumps.MenuItem(title=title, callback=callback, icon=icon)) 
            self.app.menu = [self.coins[i]]
        
        
        
    def showAll(self, sender):
        data = readJson('currentValues.json')
        i = len(data) - 1
        self.app.title = data[i]["1. Gesamtwert"] + " | " + data[i]["2. Gesamt investiert"] + " | " + data[i]["4. Prozentsatz"]

    def printNewValues(self, sender):
        self.app.title = getNewValues()
        names = getCoinNames()
        for i in range(len(names)):
            self.newButton = rumps.MenuItem(title="{}".format(names[i]), callback=self.getStats(names[i]), icon='icons/{}.png'.format(names[i]))
            self.app.menu = [self.newButton]

    def run(self):
        self.app.run()

    def getStats(self, sender, coin):
        self.app.title = coin + ": " + getSingleValues(coin)

    def printAlert():
        investments = readJson('currentValues.json')
        for i in range(len(investments) - 1):
            gewinnverlust = float(investments[i]["7. Gewinn/Verlust"].replace('EUR', ''))
            if gewinnverlust > 2 * float(investments[i]["3. Investiert"]):
                name = investments[i]["1. Coin"]
                rumps.notification(title="Einsatz verdoppelt!", subtitle='Coin {} hat sich verdoppelt!'.format(name), message='')


if __name__ == '__main__':
    app = WalletWatcherApp()
    app.run()

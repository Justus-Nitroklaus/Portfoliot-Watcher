from app.app import WalletWatcherApp
from scripts.functions import getCurrentInvestmentStats
from scripts.iconmethods import safeAllIcons
from scripts.jsonmethods import *
from app.investmentclasses import *

def main():
    emptyJsonFile('currentValues.json')
    safeAllIcons()
    storeOutputJsonData(json.dumps(getCurrentInvestmentStats(), indent = 4, sort_keys = True))

if __name__ == "__main__":
    main()
    app = WalletWatcherApp()
    app.run()

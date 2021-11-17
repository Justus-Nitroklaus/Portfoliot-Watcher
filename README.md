# Crypto Portfoliot Watcher

## Dependencies
Please clone the repository. Afterwards you can create a virtualenv if you want to, but it is not necessary.
Lastly type
```
pip install -r requirements.txt
```
You should now have all the dependencies installed.

## How it works
1. Download the dependencies as mentioned above
2. Fill your investments into investments.json

    a. The structure of the json file is an array of dictionaries: <br/>
        [ <br/>
            { <br/>
                "name": "", <br/>
                "ticker": "", <br/>
                "buys": [ <br/>
                    { <br/>
                        "amountBought": "", <br/>
                        "spent": "" <br/>
                    }
                ], <br/>
                "sold": "False", <br/>
                "sells": [ <br/>
                    { <br/>
                        "amountSold": "", <br/>
                        "price": "" <br/>
                    } <br/>
                ] <br/>
            }, ....] <br/>
        

    b. Type every floating number with a decimal point and not a comma

    c. The name of a coin has to be the name that is given on the website "https://coinmarketcap.com/currencies/{name}/"

    d. If you bought the same coin multiple times, do not calculate the average cost yourself. Just type in the amount spent and the amount of coins you received
    
    e. If you sold a coin, change the "sold" ticker to True and type the data into the "sells"-array
    
3. Start the Program from terminal with command "python __main__.py"

# import tkinter for GUI
import tkinter as tk 
from tkinter import ttk
# import json to manipulate JSON 
import json 
# import datetime for date data formats
from datetime import datetime



# Investment class, as defined in the UML diagram
class Investment:
    def __init__(self, name, purchase_price, current_price, purchase_date, investment_type):
        self.name = name
        self.purchase_price = purchase_price
        self.current_price = current_price
        self.purchase_date = purchase_date
        self.investment_type = investment_type

        # Investment methods, as defined in the UML diagram

        # calculate percent return
        def get_percent_return(self):
            percent_return = (self.currentprice - self.purchase_price) / self.purchase_price * 100
            return percent_return
        
        # retrieve current price of investment w/ API
        def update_current_price(self, price, investment_type):
            pass


# Child classes 
class Stock(Investment):
    def __init__(self, name, ticker, shares, purchase_date, purchase_price, current_price, value):
        # call parent class
        super().__init__(name =name, purchase_date=purchase_date, purchase_price=purchase_price, current_price=current_price)
        self.ticker = ticker
        self.shares = shares
        self.value = value

        # getters and setters
        def set_shares(self):
            self.shares = float(input("Enter how many shares you bought the investment at "))
        
        def set_ticker(self):
            # will use api to get ticker from name, for now label it x
            self.ticker = "x"

        # calculate abs return
        def get_abs_return(self):
            original_value = self.purchase_price * self.shares
            self.value = self.shares * self.current_price
            return self.value - original_value
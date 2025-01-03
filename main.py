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
        self.purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
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
    def __init__(self, name, ticker, shares, purchase_date, purchase_price, current_price, value, sector_type):
# call parent class
        super().__init__(name =name, purchase_date=purchase_date, purchase_price=purchase_price, current_price=current_price)
        self.ticker = ticker
        self.shares = float(shares)
        self.value = float(value)
        self.sector_type = sector_type

# getters and setters
        def set_shares(self):
            self.shares = float(input("Enter how many shares you bought the investment at "))
        
        def set_ticker(self):
            # will use api to get ticker from name, for now label it x
            self.ticker = "x"

        def set_sector_type(self):
            self.sector_type = str(input("What sector is your stock in"))

        # calculate abs return
        def get_abs_return(self):
            original_value = self.purchase_price * self.shares
            self.value = self.shares * self.current_price
            return self.value - original_value
        

class Crypto(Investment):
    def __init__(self, name, symbol, quantity, contact_address, purchase_date, purchase_price, current_price):
# call parent class
        super().__init__(name=name, purchase_date=purchase_date, purchase_price=purchase_price, current_price=current_price)
        self.symbol = symbol
        self.quantity = float(quantity)
        self.contact_address = contact_address

# getters and setters
        def set_contact_address(self):
            # will use api to get contact address from blockchain, for now label it y 
            self.contact_address = "y"

        def set_symbol(self):
            # will use api to get symbol from blockchain, for now label it x 
            self.symbol = "x"

        def get_market_cap():
            # will use api for this
            pass
        def get_24h_volume():
            # will use api for this
            pass

        def get_abs_return(self):
            original_value = self.purchase_price * self.quantity
            self.value = self.quantity * self.current_price
            return self.value - original_value
        

class ETF(Investment):
    def __init__(self, name, ticker, shares, expense_ratio, purchase_price, purchase_date, current_price):
# call parent class
        super().__init__(name=name, purchase_date=purchase_date, purchase_price=purchase_price, current_price=current_price)
        self.ticker = ticker
        self.shares = float(shares)
        self.expense_ratio = float(expense_ratio)

        # getters and setters
        def set_shares(self):
            self.shares = float(input("Enter how many shares you bought the investment at "))
        
        def set_ticker(self):
            # will use api to get ticker from name, for now label it x
            self.ticker = "x"

        def set_expense_ratio(self):
            self.expense_ratio = float(input("Enter expense ratio"))


        def get_abs_return(self):
            original_value = self.purchase_price * self.shares
            self.value = self.shares * self.current_price
            return self.value - original_value
        
        

class Portolio:
    def __init__(self):
        self.investments = []
        self.total_value = 0

    def add_investment(self, investment):
        self.investments.append(investment)

    def remove_investment(self, investment):
        self.investments.remove(investment)
    
    def calculate_total_value(self):
        return sum(investment.calculate_value() for investment in self.investments)
    

    def get_performance(self):
        pass







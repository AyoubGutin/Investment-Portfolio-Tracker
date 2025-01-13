# import tkinter for GUI
import tkinter as tk
from tkinter import ttk
# import json to manipulate JSON 
import json 
# import datetime for date data formats
from datetime import datetime
import sys

# Investment class, as defined in the UML diagram
class Investment:
    def __init__(self, name, purchase_price, current_price, purchase_date):
        self.name = name
        self.purchase_price = purchase_price
        self.current_price = current_price
        self.purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")

 # Investment methods, as defined in the UML diagram

# calculate percent return
    def get_percent_return(self):
        percent_return = (self.current_price - self.purchase_price) / self.purchase_price * 100
        return percent_return
        
# retrieve current price of investment w/ API
    def update_current_price(self, price, investment_type):
        pass


# child classes 
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
        
        

class Portfolio:
    def __init__(self, name):
        self.investments = []
        self.total_value = 0
        self.name = name

    def add_investment(self, investment):
        self.investments.append(investment)

    def remove_investment(self, investment):
        self.investments.remove(investment)
    
    def calculate_total_value(self):
        return sum(investment.calculate_value() for investment in self.investments)
    

    def get_performance(self):
        pass





def create_investment(investment_type, **kwargs):
    """
    function that takes in an investment type, and calls the respective class,
    with a number of parameters
    """
    if investment_type == "Stock":
        return Stock(**kwargs)
    elif investment_type == "ETF":
        return ETF(**kwargs)
    elif investment_type == "Crypto":
        return Crypto(**kwargs)
    else:
        print("Invalid investment type ")



# dummy data
stock_data = {
    "name": "Tesla",
    "purchase_date": "2023-01-10",
    "purchase_price": 149,
    "current_price": 170,
    "ticker": "TSLA",
    "shares": 10,
    "value": 1490,
    "sector_type": "Automobile"
}

etf_data = {
    "name": "S&P 500",
    "purchase_date": "2023-01-10",
    "purchase_price": 149,
    "current_price": 170,
    "ticker": "VOO",
    "shares": 10,
    "expense_ratio": 0.03
}

crypto_data = {
    "name": "Bitcoin",
    "purchase_date": "2023-01-10",
    "purchase_price": 150,
    "current_price": 150,
    "symbol": "BTC",
    "quantity": 1,
    "contact_address": "n/a"
}




# GUI interface
class PortfolioInterface(tk.Tk):
    def __init__(self, portfolio_list):
        super().__init__()
        self.portfolio_list = portfolio_list
        
        # title + initial res
        self.title("My Portfolio Tracker")
        self.geometry("1280x720")
        headline = ttk.Label(self, text="My Portfolio Tracker")
        subtitle = ttk.Label(self, text="You are currently signed in as 'x'")
        headline.pack()
        subtitle.pack()


        # button set up
        view_button = ttk.Button(self, text="View your portfolios", command=self.view_portfolios)
        remove_button = ttk.Button(self, text="Make a portfolio", command=self.make_portfolio)

        view_button.pack()
        remove_button.pack()


    def view_portfolios(self):
        """
        Direct to view portfolio once pressed button 
        """    

        # set up view portfolio page 
        view_portolio_window = tk.Toplevel(self)
        view_portolio_window.title("View Your Portfolios")
        view_portolio_window.geometry("1280x720")

        headline = ttk.Label(view_portolio_window, text="Your Portfolios")
        headline.pack()

        # check if list contains portfolios 
        if  len(self.portfolio_list) == 0:
            no_portfolio_exist = ttk.Label(view_portolio_window, text="No portfolios exist currently ")
            no_portfolio_exist.pack()
        else:
            for portfolio in self.portfolio_list:
                # set up the portfolio buttons, which will call on view investment method to look at the investments in that list
                portfolio_button = ttk.Button(view_portolio_window, text=portfolio.name, command= lambda p=portfolio: self.view_investments(p, view_portolio_window))
                portfolio_button.pack()
        

    def view_investments(self, portfolio, view_portolio_window):
        """
        Direct to view investment once pressed button
        """

        # child of view portfolio class
        # set up view investment page 
        view_investments_window = tk.Toplevel(view_portolio_window)
        view_investments_window.title(f"Your investments")
        view_investments_window.geometry("1280x720")

        headline = ttk.Label(view_investments_window, text=f"Investments in {portfolio.name} ")
        headline.pack()

        # check if list contains investments - this will need to have a button in the future to view *all* investments, instead of list them all in the same page. 
        if len(portfolio.investments) == 0:
            no_investments_exist = ttk.Label(view_investments_window, text="No investments exist currently ")
            no_investments_exist.pack()
        else:
            # need to add in functionality to view investments, using the portfolio class.
            pass

        # set up buttons
        add_investment_button = ttk.Button(view_investments_window, text="Add investment ", command= lambda p=portfolio: self.add_investment(p, view_investments_window))
        remove_investment_button = ttk.Button(view_investments_window, text="Remove investment ", command= lambda p=portfolio: self.remove_investment(p, view_investments_window))
        edit_investment_button = ttk.Button(view_investments_window, text="Edit investment ", command= lambda p=portfolio: self.edit_investment(p, view_investments_window))

        add_investment_button.pack()
        remove_investment_button.pack()
        edit_investment_button.pack()


    def add_investment(self, view_investments_window, portfolio):
        """
        Direct to add investment once pressed button
        """
        add_investment_window = tk.Toplevel(view_investments_window)
        add_investment_window.title(f"Add investment")
        add_investment_window.geometry("1280x720")

        headline = ttk.Label(add_investment_window, text=f"Add an investment to portfolio: {portfolio.name}")
        headline.pack()

    def remove_investment(self, view_investments_window, portfolio):
        """
        Direct to add investment once pressed button
        """
        remove_investment_window = tk.Toplevel(view_investments_window)
        remove_investment_window.title(f"Add investment")
        remove_investment_window.geometry("1280x720")

        # add functionality to remove an investment 

    def edit_investment(self, view_investments_window, portfolio):
        """
        Direct to add investment once pressed button
        """
        edit_investment_window = tk.Toplevel(view_investments_window)
        edit_investment_window.title(f"Add investment")
        edit_investment_window.geometry("1280x720")

        # add functionality to edit an investment 


    def make_portfolio(self):
        """
        Direct to make portfolio once pressed button
        """

        # set up make portfolio page 
        make_portfolio_window = ttk.Toplevel(self)
        make_portfolio_window.title("Make a portfolio")
        make_portfolio_window.geometry("1280x720")

        headline = tk.Label(make_portfolio_window, text="Make Your Portfolio ")
        headline.pack()

    
        # entry form
        enter_name = ttk.Entry(make_portfolio_window)
        enter_name.pack()
        enter_name.insert(0, "Enter a portfolio name ")

        submit_name = ttk.Button(make_portfolio_window, text="Submit ", command=lambda: self.create_portfolio(enter_name.get()))
        submit_name.pack()
        






main_portfolio = Portfolio("main")
xyz_portfolio = Portfolio("xyz")
portfolio_list = [main_portfolio, xyz_portfolio]
if __name__ == "__main__":
    app = PortfolioInterface(portfolio_list)
    app.mainloop()









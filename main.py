# import tkinter for GUI
import tkinter as tk
from tkinter import ttk, messagebox
# import json to manipulate JSON 
import json 
# import datetime for date data formats
from datetime import datetime
import sys

# -------------------
# Global Variables
# -------------------
filename = "portfolios_data.json"



# -------------------
# Define key classes 
# -------------------
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
        self.name = name
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

# -------------------
# Functions 
# -------------------

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

 
def save_portfolio_data(portfolio_list):
    portfolios_data = []

    # for loop to go through each portfolio in a list and save the investments that are in the portfolio, based on the Portfolio class
    for portfolio in portfolio_list:
        portfolio_dict = {"name": portfolio.name, "investments": []}
        # nested for loop to go through each investment in a portfolio
        for investment in portfolio.investments:
            investment_data = {
                # class of investment object, and whether it is of type <class "Stock"> etc.;
                "type": investment.__class__.__name__,
                "name": investment.name,
                "purchase_price": investment.purchase_price,
                "current_price": investment.current_price,
                # convert datetime object (what the data is stored as) into string
                "purchase_date": investment.purchase_date.strftime("%Y-%m-%d")}
        
            # if investment type is an instance of investment of type class stock/crypto/etf, then update the data with additonal entries
            if isinstance(investment, Stock):
                investment_data.update({
                    "ticker": investment.ticker,
                    "shares": investment.shares,
                    "value": investment.value,
                    "sector_type": investment.sector_type})
            if isinstance(investment, Crypto):
                investment_data.update({
                    "symbol": investment.symbol,
                    "quantity": investment.quantity,
                    "contact_address": investment.contact_address})
            elif isinstance(investment, ETF):
                investment_data.update({
                    "ticker": investment.ticker,
                    "shares": investment.shares,
                    "expense_ratio": investment.expense_ratio})
            else:
                return -1 # return error 

            # append the portfolio_dict with the updated data
            portfolio_dict["investments"].append(investment_data)
        # append the portfolio data with the dictionary when nested for loop is done
        portfolios_data.append(portfolio_dict)
        

    # save file and write the Python dictionary as JSON format 
    file = open(filename, "w+")
    json.dump(portfolios_data, file, indent=6, ensure_ascii=True)
    file.close()

    
def load_portfolio_data():
    file = open(filename, "r")

    portfolios_data = json.load(file)
    file.close()
    portfolios_list = []

    # go through each portfolio in the JSON file and load a portfolio by calling the class 
    for data in portfolios_data:
        portfolio = Portfolio(data["name"])
        # go through each attribute in investment and retrieve the investment type
        for investment_data in data["investments"]:
            investment_type = investment_data.pop("type")

            if investment_type == "Stock":
                investment = Stock(**investment_data)
            if investment_type == "Crypto":
                investment = Crypto(**investment_data)
            if investment_type == "ETF":
                investment = ETF(**investment_data)
            else:
                return -1
            portfolio.add_investment(investment)


        portfolios_list.append(portfolio)

    return portfolios_list


def load_portfolio_list():
    file = open(filename, "r")

    portfolios_data = json.load(file)
    file.close()
    portfolios_list = []

    for data in portfolios_data:
        portfolio=Portfolio(data["name"])
        portfolios_list.append(portfolio)

    return portfolios_list


# -------------------
# GUI interface
# -------------------

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
        This will be the main page of viewing list of portfolios
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
                portfolio_button = ttk.Button(view_portolio_window, text=portfolio.name, command= lambda p=portfolio: self.specific_portfolio(p, view_portolio_window))
                portfolio_button.pack()
        

    def specific_portfolio(self, portfolio, view_portolio_window):
        """
        Page that is redirected to when clicking on a portfolio. Will have several options, add/remove/edit investments, as well as viewing investments. 
        It will also have visualisations implemented. 
        """

        # child of view portfolio class
        # set up view investment page 
        specific_portfolio_window = tk.Toplevel(view_portolio_window)
        specific_portfolio_window.title(f"Your investments")
        specific_portfolio_window.geometry("1280x720")

        headline = ttk.Label(specific_portfolio_window, text=f"Investments in {portfolio.name} ")
        headline.pack()

        # check if list contains investments - this will need to have a button in the future to view *all* investments, instead of list them all in the same page. 
        if len(portfolio.investments) == 0:
            no_investments_exist = ttk.Label(specific_portfolio_window, text="No investments exist currently ")
            no_investments_exist.pack()
        else:
            # need to add in functionality to view investments, using the portfolio class.
            pass

        # set up buttons
        add_investment_button = ttk.Button(specific_portfolio_window, text="Add investment ", command= lambda p=portfolio: self.add_investment(p, specific_portfolio_window))
        remove_investment_button = ttk.Button(specific_portfolio_window, text="Remove investment ", command= lambda p=portfolio: self.remove_investment(p, specific_portfolio_window))
        edit_investment_button = ttk.Button(specific_portfolio_window, text="Edit investment ", command= lambda p=portfolio: self.edit_investment(p, specific_portfolio_window))

        add_investment_button.pack()
        remove_investment_button.pack()
        edit_investment_button.pack()

    
    def add_investment(self, portfolio, specific_portfolio_window):
        """
        This method will open up an entry form to add an investment, it will then get the data entered, and call on a function to check it.
        """
        # child of 
        add_investment_window = tk.Toplevel(specific_portfolio_window)
        add_investment_window.title(f"Add investment")
        add_investment_window.geometry("1280x720")

        headline = ttk.Label(add_investment_window, text=f"Add an investment to portfolio: {portfolio.name}")
        headline.pack()

        # Select type of investment from drop down menu, as seen in the mockup design
        tk.Label(add_investment_window, text="Investment Type ").pack()
        investment_type = tk.StringVar(value="Stock")
        dropdown_type = ttk.Combobox(add_investment_window, textvariable=investment_type, values=["Stock", "ETF", "Crypto"])
        dropdown_type.pack()

        # Rest of the inputs - in a dictionary as will have same layout / design 
        entry_form = {"Investment Name": tk.Entry(add_investment_window),
                      "Date": tk.Entry(add_investment_window),
                      "Investment Value": tk.Entry(add_investment_window),
                      "Investment Price": tk.Entry(add_investment_window)}
        
        for label, entry in entry_form.items():
            tk.Label(add_investment_window, text=label).pack()
            entry.pack()
        
        
        # Nested function to submit - this will check it the data is correct also and then save it to the portfolio
        # This will also use the function create_investment()
            def submit_investment():
                pass 
        
        submit_button = ttk.Button(add_investment_window, text="Add Investment", command=submit_investment)
        submit_button.pack()


    def remove_investment(self, portfolio, specific_portfolio_window):
        """
        Direct to add investment once pressed button
        """
        remove_investment_window = tk.Toplevel(specific_portfolio_window)
        remove_investment_window.title(f"Add investment")
        remove_investment_window.geometry("1280x720")

        # add functionality to remove an investment - will have a list of investments w/ a filter to search for

    def edit_investment(self, portfolio, specific_portfolio_window):
        """
        Direct to add investment once pressed button
        """
        edit_investment_window = tk.Toplevel(specific_portfolio_window)
        edit_investment_window.title(f"Add investment")
        edit_investment_window.geometry("1280x720")

        # add functionality to edit an investment - same as remove, will have a list of investments w/ a filter to search for


    def make_portfolio(self):
        """
        Make portfolio window
        Create a new portfolio and save it to JSON file 
        """

        # set up make portfolio page 
        make_portfolio_window = tk.Toplevel(self)
        make_portfolio_window.title("Make a portfolio")
        make_portfolio_window.geometry("1280x720") 

        headline = tk.Label(make_portfolio_window, text="Make Your Portfolio ")
        headline.pack()

    
        # entry form
        enter_name = ttk.Entry(make_portfolio_window)
        enter_name.pack()
        enter_name.insert(0, "Enter a portfolio name ")

        def submit_portfolio():
            """
            Nested function that is called when the submit button is pressed
            """
            name = enter_name.get()
            if name:
                new_portfolio = Portfolio(name)
                self.portfolio_list.append(new_portfolio)
                # save to json, just the name for now - user will be able to add investments after
                save_portfolio_data(self.portfolio_list)
                # notify user
                tk.messagebox.showinfo("Success", "Portfolio Created\nAdd investments by going back ")

        submit_name = ttk.Button(make_portfolio_window, text="Submit", command=submit_portfolio)
        submit_name.pack()









        





portfolio_list = load_portfolio_list()
if __name__ == "__main__":
    app = PortfolioInterface(portfolio_list)
    app.mainloop()









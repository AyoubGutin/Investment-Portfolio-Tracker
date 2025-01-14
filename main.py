# import tkinter for GUI
import tkinter as tk
from tkinter import ttk, messagebox
# import json to manipulate JSON 
import json 
# import datetime for date data formats
from datetime import datetime
import os

# -------------------
# Global Variables
# -------------------
filename = "portfolios_data.json"

# -------------------
# Define key classes 
# -------------------
# Investment class, as defined in the UML diagram
class Investment:
    def __init__(self, name, purchase_price, current_price, purchase_date, value):
        self.name = name
        self.purchase_price = purchase_price
        self.current_price = current_price
        self.purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
        self.value = value

 # Investment methods, as defined in the UML diagram

    def get_percent_return(self):
        """
        Calculates percentage return
        """
        percent_return = (self.current_price - self.purchase_price) / self.purchase_price * 100
        return percent_return
        
# retrieve current price of investment w/ API
    def update_current_price(self, price, investment_type):
        pass


# child classes 
class Stock(Investment):
    def __init__(self, name, purchase_date, purchase_price, current_price, value):
# call parent class
        super().__init__(name =name, purchase_date=purchase_date, purchase_price=purchase_price, current_price=current_price, value=value)

class Crypto(Investment):
    def __init__(self, name, purchase_date, purchase_price, current_price, value):
        # call parent class
        super().__init__(name=name, purchase_date=purchase_date, purchase_price=purchase_price, current_price=current_price, value=value)

class ETF(Investment):
    def __init__(self, name, purchase_price, purchase_date, current_price, value):
    # call parent class
        super().__init__(name=name, purchase_date=purchase_date, purchase_price=purchase_price, current_price=current_price, value=value)

        
class Portfolio:
    def __init__(self, name):
        self.name = name
        self.investments = []
        self.total_value = 0

    def get_investments(self, investment_data):
        """
        Loads investment from JSON, adds to portfolio
        """
        for investment in investment_data:
            investment_type = investment.pop("type")
            self.add_investment(create_investment(investment_type))

    def add_investment(self, investment):
        self.investments.append(investment)
    
    def calculate_total_value(self):
        return sum(investment.calculate_value() for investment in self.investments)
    

    def get_performance(self):
        pass

# -------------------
# Functions 
# -------------------

def create_investment(investment_type, **kwargs):
    """
    function that takes in an investment type, and calls the respective class, with a number of parameters
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
    file = open(filename, "r")
    portfolios_data = json.load(file)
    file.close()

    for portfolio in portfolio_list:
        # check if the portfolio already exists in the loaded data
        existing_portfolio = next((p for p in portfolios_data if p["name"] == portfolio.name), None)
        
        # check if any investments need to be added
        for investment in portfolio.investments:
            # if the investment doesn't exist in the portfolio, add it
            # eventually - this will update to the investment instead of not add it.
            if not any(inv['name'] == investment.name for inv in existing_portfolio["investments"]):
                investment_data = {
                    "type": investment.__class__.__name__,
                    "name": investment.name,
                    "purchase_price": investment.purchase_price,
                    "current_price": investment.current_price,
                    "purchase_date": investment.purchase_date.strftime("%Y-%m-%d")
                }
                existing_portfolio["investments"].append(investment_data)

    # Write  updated data back to  file
    file = open(filename, "w")
    json.dump(portfolios_data, file, indent=6, ensure_ascii=True)

    
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
            investment = create_investment(investment_type, **investment_data)
            portfolio.add_investment(investment)
        portfolios_list.append(portfolio)

    return portfolios_list


def load_portfolio_list():
    # Check if the file exists before loading
    if not os.path.exists(filename):
        return [] 

    file = open(filename, "r")
    portfolios_data = json.load(file)
    file.close()


    portfolios_list = []
    for data in portfolios_data:
        portfolio = Portfolio(data["name"])
        portfolios_list.append(portfolio)

    return portfolios_list


def load_investment_list(portfolio_name):
    """
    get all investments from a portfolio via JSON file 
    """
    file = open("portfolios_data.json", "r")
    data = json.load(file)
    for portfolio in data:
            if portfolio["name"] == portfolio_name:
                return portfolio.get("investments", [])
            else:
                return []
                

def update_investment(portfolio_name, updated_investments):
    file = open("portfolios_data.json", "r")
    data = json.load(file)
    file.close()

    for portfolio in data:
        if portfolio["name"] == portfolio_name:
            portfolio["investments"] = updated_investments 
        
    file = open("portfolios_data.json", "w")
    json.dump(data, file, indent=6)
    file.close()
        
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


        # call on load investment function 
        investments = load_investment_list(portfolio.name)

        # check if list contains investments - this will need to have a button in the future to view *all* investments, instead of list them all in the same page. 
        if len(investments) == 0:
            no_investments_exist = ttk.Label(specific_portfolio_window, text="No investments exist currently ")
            no_investments_exist.pack()
        else:
            for investment in investments:
                investment_display = ttk.Label(specific_portfolio_window, text=investment)
                investment_display.pack()

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
            # get the entries once button is pressed
            name = entry_form["Investment Name"].get()
            purchase_date = entry_form["Date"].get()
            value = entry_form["Investment Value"].get()
            purhase_price = float(entry_form["Investment Price"].get())
            type = investment_type.get()

            # create investment object
            investment_data = {
                "name": name,
                "purchase_date": purchase_date,
                "value": value,
                "purchase_price": purhase_price,
                "current_price": purhase_price # keep current price as purchase price for now 
            }

            investment = create_investment(type, **investment_data)

            # add investment to portfolio
            portfolio.add_investment(investment)

            # save to JSON
            save_portfolio_data(self.portfolio_list)

            # notify user
            tk.messagebox.showinfo("Success", "Investment created")

        submit_button = ttk.Button(add_investment_window, text="Add Investment", command=submit_investment)
        submit_button.pack()


    def remove_investment(self, portfolio, specific_portfolio_window):
        """
        Direct to add investment once pressed button
        """
        
        # intialise screen
        remove_investment_window = tk.Toplevel(specific_portfolio_window)
        remove_investment_window.title(f"Add investment")
        remove_investment_window.geometry("1280x720")

        investments = load_investment_list(portfolio.name)

        # nested method for removal, once an investment is selected 
        def removal(investment):
            """
            Remove selected investment 
            """
            if investment in investments:
                investments.remove(investment)
                update_investment(portfolio.name, investments)
                messagebox.showinfo("Success", "Removed investment")
        
        # display investment in a listbox to remove
        select_investment = ttk.Label(remove_investment_window, text="Select investment to remove ")
        select_investment.pack()
    

        listbox = tk.Listbox(remove_investment_window, height=20, width=100)
        for investment in investments:
            investment_det = {
                f"Type: {investment['type']}, ",
                f"Name: {investment['name']}, "
            }
            listbox.insert(tk.END, investment_det)
        listbox.pack()
        
        # remove button 
        remove_button = ttk.Button(remove_investment_window, text="Remove", 
                                   command = lambda: removal(investments[listbox.curselection()[0]]))
        remove_button.pack()


    def edit_investment(self, portfolio, specific_portfolio_window):
        """
        Direct to add investment once pressed button
        """
        edit_investment_window = tk.Toplevel(specific_portfolio_window)
        edit_investment_window.title(f"Edit investment")
        edit_investment_window.geometry("1280x720")

        # same as remove, will have a list of investments.
        
        investments = load_investment_list(portfolio.name)

        def edit(investment):
            """
            Edit investment selected
            """
            edit_window = tk.Toplevel(edit_investment_window)
            edit_window.title("Edit Investment ")
            edit_window.geometry("720x400")

            # pre fill 
            tk.Label(edit_window, text="Type").pack()
            type_entry = tk.Entry(edit_window)
            type_entry.insert(0, investment["type"])
            type_entry.pack()

            tk.Label(edit_window, text="Name").pack()
            name_entry = tk.Entry(edit_window)
            name_entry.insert(0, investment["name"])
            name_entry.pack()

            tk.Label(edit_window, text="Purchase Price").pack()
            pp_entry = tk.Entry(edit_window)
            pp_entry.insert(0, investment["purchase_price"])
            pp_entry.pack()

            tk.Label(edit_window, text="Purchase Date").pack()
            pd_entry = tk.Entry(edit_window)
            pd_entry.insert(0, investment["purchase_date"])
            pd_entry.pack()


            def save_changes():
                """
                Get fields once button pressed
                """
                investment["type"] = type_entry.get()
                investment["name"] = name_entry.get()
                investment["purchase_price"] = float(pp_entry.get())
                investment["purchase_date"] = pd_entry.get()

                update_investment(portfolio.name, investments)
                messagebox.showinfo("Success", "Investment Updated")
        
            save_button = ttk.Button(edit_window, text="Save", command=save_changes)
            save_button.pack()
    

        select_investment = ttk.Label(edit_investment_window, text="Select investment to remove ")
        select_investment.pack()
    

        listbox = tk.Listbox(edit_investment_window, height=20, width=100)
        for investment in investments:
            investment_det = {
                f"Type: {investment['type']}, Name: {investment['name']}"
            }
            listbox.insert(tk.END, investment_det)
        listbox.pack()

        edit_button = ttk.Button(edit_investment_window, text="Edit", command= lambda: edit(investments[listbox.curselection()[0]]))
        edit_button.pack()


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









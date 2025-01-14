# import tkinter for GUI
import tkinter as tk
from tkinter import ttk, messagebox
# import json to manipulate JSON 
import json 
# import datetime for date data formats
from datetime import datetime
import os
# visualisation 
import matplotlib.pyplot as plt 

# -------------------
# Global Variables
# -------------------
filename = "portfolios_data.json"
background = "#d3d3d3"
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
    def update_current_price(self):
        print("Not added")
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
    """
    function that saves data of a portfolio by converting from JSON to Object code, so it is readable by the program, then checks if there's any pending investments to be added once the check is complete, the function then writes the investments into the JSON file and closes the file, therefore saving the data of the portfolio so it not lost after session
    """
    file = open(filename, "r")
    portfolios_data = json.load(file)
    file.close()

    for portfolio in portfolio_list:
        # check if the portfolio already exists in the loaded data, if not make one
        existing_portfolio = next((p for p in portfolios_data if p["name"] == portfolio.name), None)
        if existing_portfolio == None:
            existing_portfolio = {
                "name": portfolio.name,
                "investments": []
            }
            portfolios_data.append(existing_portfolio)
        
        # check if any investments need to be added
        for investment in portfolio.investments:
            # if the investment doesn't exist in the portfolio, add it
            # eventually - this will update to the investment instead of not add it.
            if not any(inv["name"] == investment.name for inv in existing_portfolio["investments"]):
                investment_data = {
                    "type": investment.__class__.__name__,
                    "name": investment.name,
                    "purchase_price": investment.purchase_price,
                    "value": investment.value,
                    "current_price": investment.current_price,
                    "purchase_date": investment.purchase_date.strftime("%Y-%m-%d")
                }
                existing_portfolio["investments"].append(investment_data)

    # write updated data back to  file
    file = open(filename, "w")
    json.dump(portfolios_data, file, indent=6, ensure_ascii=True)

def load_portfolio_data():
    """
    this returns a list of portolios with their respective data.
    """
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
    """
    this loads only a list of portfolios, not the data - used when wanting to view a list of portfolios currently 
    """
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
    this loads only a list of investments, not objects, so methods can't be used - used when wanting to view a list of investments currently in a portfolio
    """
    file = open("portfolios_data.json", "r")
    data = json.load(file)
    print(data)
    for portfolio in data:
            print(portfolio)
            if portfolio["name"] == portfolio_name:
                return portfolio.get("investments", [])
            else:
                return []

def load_investment_object(portfolio_name):
    """
    this loads JSON data and retrieves data about invesments, then converts to object code, so methods can be used.
    """
    file = open("portfolios_data.json", "r")
    data = json.load(file)
    file.close()
    for portfolio in data:
            if portfolio["name"] == portfolio_name:
                investments = portfolio.get("investments", [])
                investment_objects = []
                for investment_data in investments:
                    investment_type = investment_data.pop("type")
                    investment_object = create_investment(investment_type, **investment_data)
                    investment_objects.append(investment_object)
                return investment_objects
            else:
                return []

def update_investment(portfolio_name, updated_investments):
    """
    this adds investments to the JSON file
    """
    file = open("portfolios_data.json", "r")
    data = json.load(file)
    file.close()

    for portfolio in data:
        if portfolio["name"] == portfolio_name:
            portfolio["investments"] = updated_investments 
        
    file = open("portfolios_data.json", "w")
    json.dump(data, file, indent=6)
    file.close()


def update_all_prices(portfolio, portfolio_list):
    """
    this function updates  prices by calling on the investment method. Currently, feature is WIP 
    """
    tk.messagebox.showinfo("Failure", "Feature not added")
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
        self.configure(bg=background)

        headline = tk.Label(self, text="My Portfolio Tracker",
                             font=("Arial Black", 28), bg=background, fg="black")
        subtitle = tk.Label(self, text="You are currently signed in as GUEST",
                             font=("Arial", 14), bg=background, fg="black")
        headline.pack(pady=(55,15))
        subtitle.pack(pady=(0,35))


        # button set up
        view_button = tk.Button(self, text="View your portfolios", command=self.view_portfolios,
                                 font=("Arial", 16), bg="black", fg="white", relief="flat", width=20, height=5)
        remove_button = tk.Button(self, text="Make a portfolio", command=self.make_portfolio,
                                   font=("Arial", 16), bg="black", fg="white", relief="flat", width=20, height=5)

        view_button.pack(pady=15)
        remove_button.pack(pady=15)

    def view_portfolios(self):
        """
        This will be the main page of viewing list of portfolios
        """    

        # set up view portfolio page 
        view_portolio_window = tk.Toplevel(self)
        view_portolio_window.title("View Your Portfolios")
        view_portolio_window.geometry("1280x720")
        view_portolio_window.configure(bg=background)

        headline = tk.Label(view_portolio_window, text="Your Portfolios",
                             font=("Arial Black", 28), bg=background, fg="black")
        headline.pack(pady=(55,15))

        # check if list contains portfolios 
        if  len(self.portfolio_list) == 0:
            no_portfolio_exist = tk.Label(view_portolio_window, text="No portfolios exist currently",
                                           font=("Arial Black", 20), bg=background, fg="black")
            no_portfolio_exist.pack()
        else:
            for portfolio in self.portfolio_list:
                # set up the portfolio buttons, which will call on view investment method to look at the investments in that list
                portfolio_button = tk.Button(view_portolio_window, text=portfolio.name, command= lambda p=portfolio: self.specific_portfolio(p, view_portolio_window),
                                            font=("Arial", 16), bg="black", fg="white", relief="flat", width=20, height=5)
                portfolio_button.pack(pady=15)

    def specific_portfolio(self, portfolio, view_portolio_window):
        """
        Page that is redirected to when clicking on a portfolio. Will have several options, add/remove/edit investments, as well as viewing investments. It will also have visualisations implemented. 
        """
        # child of view portfolio class
        # set up view investment page 
        specific_portfolio_window = tk.Toplevel(view_portolio_window)
        specific_portfolio_window.title(f"Your investments")
        specific_portfolio_window.geometry("1280x720")
        specific_portfolio_window.configure(bg=background)

        headline = tk.Label(specific_portfolio_window, text=f"Investments in {portfolio.name}",
                             font=("Arial Black", 28), bg=background, fg="black")
        headline.pack(pady=(55,15))

        # call on load investment function 
        investments = load_investment_list(portfolio.name)

        # nested function to show performance of investments 
        def show_performance():
            """
            Display performance of all investments
            """
            # bar chart prep
            investments = load_investment_list(portfolio.name)
            names = []
            purchase_price = []
            current_price = []
            percent_returns = []

            for investment in investments:
                names.append(investment["name"])
                purchase_price.append(investment["purchase_price"])
                current_price.append(investment["current_price"])

                        # calculate percentage return directly
                percent_return = ((investment["current_price"] - investment["purchase_price"]) / investment["purchase_price"]) * 100
                percent_returns.append(percent_return)

            # create bar chart
            x = range(len(names))
            fig, ax = plt.subplots()

            bar_width = 0.5
            ax.bar(x, purchase_price, bar_width, label="Purchase Price")
            ax.bar([p + bar_width for p in x], current_price, bar_width, label="Current Price")

            ax.set_xlabel("Investments")
            ax.set_ylabel("Price")
            ax.set_title("Investment Performanece")
            ax.set_xticks([p + bar_width /2 for p in x])
            # show name
            ax.set_xticklabels(names, rotation=45, ha="right")
            ax.legend()

            for i, name in enumerate(names):
                # display percentage return
                percent_return = percent_returns[i]
                print(percent_return)
                ax.text(i, max(purchase_price[i], current_price[i]) + 2, f"{percent_return:.2f}%", ha="center", va="bottom", fontsize=10, color="blue")
            plt.show()

        # set up table for viewing investments
        tree = ttk.Treeview(specific_portfolio_window, columns=("Type", "Name", "Purchase Price", "Current Price", "Value", "Purchase Date"), show="headings")
        tree.heading("Type", text="Type")
        tree.heading("Name", text="Name")
        tree.heading("Purchase Price", text="Purchase Price")
        tree.heading("Current Price", text="Current Price")
        tree.heading("Value", text="Value")
        tree.heading("Purchase Date", text="Purchase Date")

        tree.column("Type", width=100)
        tree.column("Name", width=100)
        tree.column("Purchase Price", width=100)
        tree.column("Current Price", width=100)
        tree.column("Value", width=100)
        tree.column("Purchase Date", width=100)

        # check if list contains investments - this will need to have a button in the future to view *all* investments, instead of list them all in the same page. 
        if len(investments) == 0:
            no_investments_exist = tk.Label(specific_portfolio_window, text="No investments exist currently ",
                                            font=("Arial", 14), bg=background, fg="black")
            no_investments_exist.pack(pady=(0,15))
        else:
            for investment in investments:
                tree.insert("", tk.END, values=(investment["type"], investment["name"], investment["purchase_price"], investment["current_price"], investment["value"], investment["purchase_date"]))
        tree.pack(fill=tk.BOTH, expand=True)

        def apply_filter():
            filter = filter_entry.get().lower()
            for row in tree.get_children():
                tree.delete(row)
            # insert row match filter
            for investment in investments:
                if filter in investment["name"].lower():
                    tree.insert("", tk.END, values=(investment["type"], investment["name"], investment["purchase_price"], investment["current_price"], investment["value"], investment["purchase_date"]))

        # frame for filter
        filter_frame = tk.Frame(specific_portfolio_window, bg=background)
        filter_frame.pack(pady=15)

        filter_label = tk.Label(filter_frame, text="Filter by Name: ", bg=background,
                                font=("Arial", 16))
        filter_label.pack(side=tk.LEFT, padx=8)

        filter_entry = tk.Entry(filter_frame, font=("Arial", 16))
        filter_entry.pack(side=tk.LEFT, padx=8)

        filter_button = tk.Button(filter_frame, text="Apply",
                                   command=apply_filter, font=("Arial", 16), bg="black", fg="white", 
                                   relief="flat", width=10)
        filter_button.pack(side=tk.LEFT, padx=10)

        # set up buttons
        add_investment_button = tk.Button(specific_portfolio_window, text="Add investment ", command= lambda p=portfolio: self.add_investment(p, specific_portfolio_window),
                                          font=("Arial", 10), bg="black", fg="white", relief="flat", width=20, height=1)
        remove_investment_button = tk.Button(specific_portfolio_window, text="Remove investment ", command= lambda p=portfolio: self.remove_investment(p, specific_portfolio_window),
                                              font=("Arial", 10), bg="black", fg="white", relief="flat", width=20, height=1)
        edit_investment_button = tk.Button(specific_portfolio_window, text="Edit investment ", command= lambda p=portfolio: self.edit_investment(p, specific_portfolio_window),
                                            font=("Arial", 10), bg="black", fg="white", relief="flat", width=20, height=1)
        update_prices_button = tk.Button(specific_portfolio_window, text="Update prices", command=lambda p=portfolio: update_all_prices(p, self.portfolio_list,),
                                          font=("Arial", 10), bg="black", fg="white", relief="flat", width=20, height=1)
        show_performance_button = tk.Button(specific_portfolio_window, text="Show performance", command = show_performance,
                                             font=("Arial", 10), bg="black", fg="white", relief="flat", width=20, height=1)

        add_investment_button.pack(pady=5)
        remove_investment_button.pack(pady=5)
        edit_investment_button.pack(pady=5)
        update_prices_button.pack(pady=5)
        show_performance_button.pack(pady=5)

    def add_investment(self, portfolio, specific_portfolio_window):
        """
        This method will open up an entry form to add an investment, it will then get the data entered, and call on a function to check it.
        """
        add_investment_window = tk.Toplevel(specific_portfolio_window)
        add_investment_window.title(f"Add investment")
        add_investment_window.geometry("1280x720")
        add_investment_window.configure(bg=background)

        headline = tk.Label(add_investment_window, text=f"Add an investment to portfolio: {portfolio.name}",
                             font=("Arial Black", 28), bg=background, fg="black")
        headline.pack(pady=(55,15))

        # select type of investment from drop down menu, as seen in the mockup design
        tk.Label(add_investment_window, text="Investment Type ").pack()
        investment_type = tk.StringVar(value="Stock")
        dropdown_type = ttk.Combobox(add_investment_window, textvariable=investment_type, values=["Stock", "ETF", "Crypto"])
        dropdown_type.pack()

        # rest of the inputs - in a dictionary as will have same layout / design 
        entry_form = {"Investment Name": tk.Entry(add_investment_window),
                      "Date": tk.Entry(add_investment_window),
                      "Investment Value": tk.Entry(add_investment_window),
                      "Investment Price": tk.Entry(add_investment_window),
                      "Current Price": tk.Entry(add_investment_window)}
        
        for label, entry in entry_form.items():
            tk.Label(add_investment_window, text=label).pack()
            entry.pack()
        
        # nested function to submit - this will check it the data is correct also and then save it to the portfolio
        # this will also use the function create_investment()
        def submit_investment():
            # get the entries once button is pressed
            name = entry_form["Investment Name"].get()
            purchase_date = entry_form["Date"].get()
            value = entry_form["Investment Value"].get()
            purchase_price = float(entry_form["Investment Price"].get())
            current_price = float(entry_form["Current Price"].get())
            type = investment_type.get()

            # create investment object
            investment_data = {
                "name": name,
                "purchase_date": purchase_date,
                "value": value,
                "purchase_price": purchase_price,
                "current_price": current_price # keep current price as purchase price for now 
            }
            investment = create_investment(type, **investment_data)

            # add investment to portfolio
            portfolio.add_investment(investment)

            # save to JSON
            save_portfolio_data(self.portfolio_list)

            # notify user
            tk.messagebox.showinfo("Success", "Investment created")

        submit_button = tk.Button(add_investment_window, text="Add Investment", command=submit_investment, font=("Arial", 16), bg="black", fg="white", relief="flat", width=20, height=5)
        submit_button.pack(pady=15)

    def remove_investment(self, portfolio, specific_portfolio_window):
        """
        Removes investment
        """
        # intialise screen
        remove_investment_window = tk.Toplevel(specific_portfolio_window)
        remove_investment_window.title(f"Add investment")
        remove_investment_window.geometry("1280x720")
        remove_investment_window.configure(bg=background)

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
        remove_button = tk.Button(remove_investment_window, text="Remove", 
                                   command = lambda: removal(investments[listbox.curselection()[0]]),
                                   font=("Arial", 16), bg="black", fg="white", relief="flat", width=20, height=5)
        remove_button.pack(pady=15)

    def edit_investment(self, portfolio, specific_portfolio_window):
        """
        Direct to add investment once pressed button
        """
        edit_investment_window = tk.Toplevel(specific_portfolio_window)
        edit_investment_window.title(f"Edit investment")
        edit_investment_window.geometry("1280x720")
        edit_investment_window.configure(bg=background)

        # same as remove, will have a list of investments.
        
        investments = load_investment_list(portfolio.name)

        def edit(investment):
            """
            Edit investment selected
            """
            edit_window = tk.Toplevel(edit_investment_window)
            edit_window.title("Edit Investment ")
            edit_window.geometry("720x400")
            self.configure(bg=background)

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

            
            tk.Label(edit_window, text="Current Price").pack()
            cp_entry = tk.Entry(edit_window)
            cp_entry.insert(0, investment["current_price"])
            cp_entry.pack()

            def save_changes():
                """
                Get fields once button pressed
                """
                investment["type"] = type_entry.get()
                investment["name"] = name_entry.get()
                investment["purchase_price"] = float(pp_entry.get())
                investment["purchase_date"] = pd_entry.get()
                investment["current_price"] = cp_entry.get()

                update_investment(portfolio.name, investments)
                messagebox.showinfo("Success", "Investment Updated")
        
            save_button = tk.Button(edit_window, text="Save", command=save_changes,
                                    font=("Arial", 16), bg="black", fg="white", relief="flat", width=20, height=5)
            save_button.pack(pady=15)
    

        select_investment = ttk.Label(edit_investment_window, text="Select investment to remove ")
        select_investment.pack()
    
        listbox = tk.Listbox(edit_investment_window, height=20, width=100)
        for investment in investments:
            investment_det = {
                f"Type: {investment['type']}, Name: {investment['name']}"
            }
            listbox.insert(tk.END, investment_det)
        listbox.pack()

        edit_button = tk.Button(edit_investment_window, text="Edit", command= lambda: edit(investments[listbox.curselection()[0]]),
                                font=("Arial", 16), bg="black", fg="white", relief="flat", width=20, height=5)
        edit_button.pack(pady=15)

    def make_portfolio(self):
        """
        Make portfolio window
        Create a new portfolio and save it to JSON file 
        """

        # set up make portfolio page 
        make_portfolio_window = tk.Toplevel(self)
        make_portfolio_window.title("Make a portfolio")
        make_portfolio_window.geometry("1280x720") 
        make_portfolio_window.configure(bg=background)

        headline = tk.Label(make_portfolio_window, text="Make Your Portfolio ",
                             font=("Arial Black", 28), bg=background, fg="black")
        headline.pack(pady=(55,15))

        # entry form
        enter_name = ttk.Entry(make_portfolio_window)
        enter_name.pack(pady=15)
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

        submit_name = tk.Button(make_portfolio_window, text="Submit", command=submit_portfolio, font=("Arial", 16), bg="black", fg="white", relief="flat", width=20, height=5)
        submit_name.pack(pady=15)

# Main code that will be run 
portfolio_list = load_portfolio_list()
if __name__ == "__main__":
    app = PortfolioInterface(portfolio_list)
    app.mainloop()
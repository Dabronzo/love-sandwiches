import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get the imput sales data from user
    """
    while True:
        print("Please, enter the sales numbers from the last market")
        print("The input shall be a list of six numbers with a ',' as separator")
        print("Exemple: 10,20,30,40,50,60\n")

        data_str = input("Enter yout data here: ")
        sales_data = data_str.split(',')
        if validate_data(sales_data):
            print("Data is valid!")
            break
    return sales_data

def validate_data(values):
    """
    Inside of try convert the values to integer
    Raise ValueError if cannot be convertet, or the input has not precisely six values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Your input has {len(values)} values, exactly 6 are required"
            )
    except ValueError as e:
        print(f"Invalid data {e}. Please try again.\n")
        return False

    return True

def update_worksheet(data, worksheet):
    """
    Update the worksheet depending on the worksheet name as argument
    """
    print(f"Updating {worksheet}..\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print("The worksheep was sucessfully updated..\n")


def calculate_surplus_data(sales_row):
    """
    Compare the sales with the stock and return a surplus of each type
    
    Surplus is defined with the sales subtracted from the stock
    positive surplus indicate waste
    negative surplus indicate extra made
    """
    print("Calculating surplus data..\n")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_rowll = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_rowll, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data

def get_sales_column_data():
    """
    Gets the last 5 entries to of the columns
    on the sales worksheet
    """
    sales = SHEET.worksheet('sales')
    # column = sales.col_values(3)
    # print(column[-5])

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    Calculate the average with the last 5 itens of the sales
    """
    print("Calculating stock data...\n")
    new_stock_data = []
    
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_numb = average * 1.1
        new_stock_data.append(round(stock_numb))
    return new_stock_data

def main():
    """
    Main function to call the all the program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    sales_column = get_sales_column_data()
    stock_data = calculate_stock_data(sales_column)
    update_worksheet(stock_data, 'stock')
    




print("Welcome to LoveSandwiches Data Automation.\n")
main()



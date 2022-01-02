import gspread
from google.oauth2.service_account import Credentials

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
    print("Please, enter the sales numbers from the last market")
    print("The input shall be a list of six numbers with a ',' as separator")
    print("Exemple: 10,20,30,40,50,60\n")

    data_str = input("Enter yout data here: ")
    sales_data = data_str.split(',')
    validate_data(sales_data)


def validate_data(values):
    """
    Inside of try convert the values to integer
    Raise ValueError if cannot be convertet, or the input has not precisely six values
    """
    try:
        if len(values) != 6:
            raise ValueError(
                f"Your input has {len(values)} values, exactly 6 are required"
            )
    except ValueError as e:
        print(f"Invalid data {e}. Please try again.\n")


get_sales_data()

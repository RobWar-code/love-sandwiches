import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

sales = SHEET.worksheet("sales")


def get_sales_data():
    """
        Get sales data from the user
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers separated by commas.")
        print("Example 10,20,30,40,50,60\n")

        str_data = input("Enter your data here:")

        sales_data = str_data.split(",")
        if validate_data(sales_data):
            print("Data valid")
            break

    return sales_data


def validate_data(values):
    """
        Inside the try, convert all values to integer
        Raises ValueError if values cannot be converted to int
        Checks that there ar exactly six values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly six values must be given, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data entered: {e}, please try again\n")
        return False

    return True


data = get_sales_data()

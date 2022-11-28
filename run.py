from pprint import pprint
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


def update_worksheet(data, worksheet):
    """
        Append a row of data to the given worksheet
    """
    print(f"Updating {worksheet} worksheet...\n")

    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"Worksheet {worksheet} updated successfully\n")


def calculate_surplus_data(sales_row):
    """
        Calculate the surplus stock from the sales data

        The surplus is the stock minus sales
        Negative values: shortfall of stock
        Positive values: waste
    """
    print("Calculating Surplus Data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_last_five_entries_sales():
    """
        Get the last five entries from the sales worksheet
        and return as a list of lists
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    pprint(columns)


def main():
    """
        Perform all the functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")


print("Welcome to Love Sandwiches Stock Automation\n")
# main()
get_last_five_entries_sales()

from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}


def get_date(prompt, allow_default=False):
    if allow_default:
        return datetime.today().strftime(date_format)

    while True:
        date_str = input(prompt)
        try:
            valid_date = datetime.strptime(date_str, date_format)
            return valid_date.strftime(date_format)
        except ValueError:
            print("❌ Invalid format! Use dd-mm-yyyy")


def get_amount():
    while True:
        try:
            amount = float(input("Enter amount: "))
            if amount > 0:
                return amount
            else:
                print("❌ Amount must be positive.")
        except ValueError:
            print("❌ Invalid input! Enter a number.")


def get_category():
    while True:
        category = input("Enter category ('I' for Income, 'E' for Expense): ").upper()
        if category in CATEGORIES:
            return CATEGORIES[category]
        print("❌ Invalid choice! Use 'I' or 'E'.")


def get_description():
    return input("Enter description (optional): ")

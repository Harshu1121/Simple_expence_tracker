import pandas as pd
import csv
from datetime import datetime

class TransactionHandler:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        """Creates a CSV file if it doesn't exist."""
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        """Adds a new transaction entry to the CSV file."""
        new_entry = {"date": date, "amount": amount, "category": category, "description": description}
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)

    @classmethod
    def get_transactions(cls, start_date, end_date):
        """Retrieves transactions within a date range."""
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)

        filtered_df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
        return filtered_df if not filtered_df.empty else pd.DataFrame(columns=cls.COLUMNS)

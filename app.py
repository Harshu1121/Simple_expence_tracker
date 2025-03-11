import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from transaction_handler import TransactionHandler
from data_entry import get_date, get_amount, get_category, get_description

# Initialize the transaction handler
TransactionHandler.initialize_csv()

# Streamlit UI
st.title("💰 Personal Finance Tracker")

# Menu options
menu = st.sidebar.radio("Navigation", ["Add Transaction", "View Transactions & Summary"])

if menu == "Add Transaction":
    st.header("📌 Add a New Transaction")

    # User inputs
    date = st.text_input("Enter date (dd-mm-yyyy) or leave blank for today:", get_date("", allow_default=True))
    amount = st.number_input("Enter amount:", min_value=0.01, format="%.2f")
    category = st.selectbox("Select category:", ["Income", "Expense"])
    description = st.text_area("Enter description (optional):")

    if st.button("Add Transaction"):
        TransactionHandler.add_entry(date, amount, category, description)
        st.success("✅ Transaction added successfully!")

elif menu == "View Transactions & Summary":
    st.header("📊 View Transactions & Summary")

    start_date = st.text_input("Enter start date (dd-mm-yyyy):")
    end_date = st.text_input("Enter end date (dd-mm-yyyy):")

    if st.button("Show Transactions"):
        if start_date and end_date:
            df = TransactionHandler.get_transactions(start_date, end_date)

            if not df.empty:
                st.write("### Transactions")
                st.dataframe(df)

                # Summary
                total_income = df[df["category"] == "Income"]["amount"].sum()
                total_expense = df[df["category"] == "Expense"]["amount"].sum()
                net_savings = total_income - total_expense

                st.write("### Summary")
                st.metric(label="Total Income", value=f"${total_income:.2f}")
                st.metric(label="Total Expense", value=f"${total_expense:.2f}")
                st.metric(label="Net Savings", value=f"${net_savings:.2f}")

                # Plot transactions
                df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
                df.set_index("date", inplace=True)

                st.write("### Income & Expense Trends")
                fig, ax = plt.subplots(figsize=(10, 5))
                df[df["category"] == "Income"]["amount"].plot(ax=ax, label="Income", color="g")
                df[df["category"] == "Expense"]["amount"].plot(ax=ax, label="Expense", color="r")
                ax.set_xlabel("Date")
                ax.set_ylabel("Amount")
                ax.legend()
                ax.grid()
                st.pyplot(fig)
        else:
            st.warning("⚠️ Please enter both start and end dates.")

# budget_tracker_portfolio.py

import streamlit as st
import pandas as pd
from datetime import datetime

# -------------------------------
# Page config
st.set_page_config(
    page_title="Portfolio Budget Tracker",
    page_icon="💰",
    layout="wide"
)

# -------------------------------
# Initialize session state
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=["Type", "Category", "Amount", "Date"])

# -------------------------------
# Minimalist CSS styling
st.markdown("""
<style>
body {
    background-color: #ffffff;
    font-family: 'Helvetica', sans-serif;
    color: #111111;
}
h1 {
    font-weight: 700;
    color: #111111;
}
.stButton>button {
    background-color: #000000;
    color: #ffffff;
    border-radius: 6px;
    height: 40px;
    width: 100%;
    font-size: 16px;
}
.stButton>button:hover {
    background-color: #333333;
}
input, select {
    padding: 0.5rem;
    margin-bottom: 0.5rem;
    border-radius: 5px;
    border: 1px solid #ccc;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Header
st.title("💼 Portfolio Budget Tracker")
st.markdown("Minimalist and interactive — perfect for your portfolio.")

# -------------------------------
# Sidebar for adding transactions
st.sidebar.header("Add Transaction")
transaction_type = st.sidebar.selectbox("Type", ["Income", "Expense"])
category = st.sidebar.text_input("Category (e.g., Salary, Food, Rent)", "")
amount_input = st.sidebar.text_input("Amount")
date = st.sidebar.date_input("Date", value=datetime.today())

add_button = st.sidebar.button("Add Transaction")
clear_button = st.sidebar.button("Clear All Transactions")

# -------------------------------
# Functions to handle transactions
def add_transaction():
    try:
        amount = float(amount_input)
    except:
        amount = None
    if not category:
        st.sidebar.error("⚠️ Please enter a category")
    elif amount is None:
        st.sidebar.error("⚠️ Enter a valid number")
    else:
        new_trx = {"Type": transaction_type, "Category": category, "Amount": amount, "Date": date}
        st.session_state.transactions = pd.concat([st.session_state.transactions, pd.DataFrame([new_trx])], ignore_index=True)
        st.success(f"{transaction_type} added!")

def clear_transactions():
    st.session_state.transactions = pd.DataFrame(columns=["Type", "Category", "Amount", "Date"])
    st.warning("All transactions cleared!")

if add_button:
    add_transaction()

if clear_button:
    clear_transactions()

# -------------------------------
# Display transaction table
if not st.session_state.transactions.empty:
    st.subheader("📊 Transaction History")
    st.dataframe(st.session_state.transactions)

    # Summary metrics
    total_income = st.session_state.transactions[st.session_state.transactions["Type"]=="Income"]["Amount"].sum()
    total_expense = st.session_state.transactions[st.session_state.transactions["Type"]=="Expense"]["Amount"].sum()
    net_balance = total_income - total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("💵 Total Income", f"${total_income:,.2f}")
    col2.metric("💸 Total Expenses", f"${total_expense:,.2f}")
    col3.metric("🧾 Net Balance", f"${net_balance:,.2f}")

    # Charts
    st.subheader("📈 Visual Summary")
    chart_data = st.session_state.transactions.groupby(["Type","Category"])["Amount"].sum().unstack().fillna(0)
    st.bar_chart(chart_data)

else:
    st.info("No transactions yet. Add income or expenses from the sidebar.")
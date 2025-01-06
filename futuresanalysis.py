import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Function to calculate Binance-like analysis
def calculate_binance_analysis(df):
    # Normalize column names
    df.columns = df.columns.str.strip()  # Remove extra spaces
    df.columns = df.columns.str.lower()  # Convert to lowercase
    df.columns = df.columns.str.replace(' ', '_')  # Replace spaces with underscores

    # Ensure required columns exist
    required_columns = ['time(utc)', 'realized_profit', 'amount', 'fee', 'funding_fee', 'balance']
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0  # Default to 0 if column is missing

    # Convert 'Time(UTC)' to datetime
    df['time(utc)'] = pd.to_datetime(df['time(utc)'])

    # Calculate Account Balance
    account_balance = df['balance'].iloc[-1]  # Latest balance

    # Calculate Realized PNL
    realized_pnl = df['realized_profit'].sum()

    # Calculate Funding Fees
    total_funding_fee = df['funding_fee'].sum()

    # Calculate Transaction Fees
    total_transaction_fee = df['fee'].sum()

    # Calculate Trading Activity
    today = datetime.utcnow().date()
    last_7d = today - timedelta(days=7)
    last_30d = today - timedelta(days=30)

    daily_trading_volume = df[df['time(utc)'].dt.date == today]['amount'].sum()
    weekly_trading_volume = df[df['time(utc)'].dt.date >= last_7d]['amount'].sum()
    monthly_trading_volume = df[df['time(utc)'].dt.date >= last_30d]['amount'].sum()

    # Return the results as a dictionary
    return {
        "Account Balance": account_balance,
        "Realized PNL": realized_pnl,
        "Total Funding Fee": total_funding_fee,
        "Total Transaction Fee": total_transaction_fee,
        "Daily Trading Volume": daily_trading_volume,
        "Weekly Trading Volume": weekly_trading_volume,
        "Monthly Trading Volume": monthly_trading_volume
    }

# Streamlit App
st.title("Binance Futures Wallet Balance Analysis")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file with encoding='utf-8-sig' to handle BOM
    df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
    
    # Display the uploaded data
    st.write("Uploaded Data:")
    st.write(df)
    
    # Calculate Binance-like Analysis
    analysis_results = calculate_binance_analysis(df)
    
    # Display Account Balance
    st.write("### Account Balance")
    st.write(f"**Current Balance:** {analysis_results['Account Balance']:.2f} USD")

    # Display PNL Analysis
    st.write("### PNL Analysis")
    st.write(f"**Realized PNL:** {analysis_results['Realized PNL']:.2f} USD")

    # Display Fee Analysis
    st.write("### Fee Analysis")
    st.write(f"**Total Funding Fee:** {analysis_results['Total Funding Fee']:.2f} USD")
    st.write(f"**Total Transaction Fee:** {analysis_results['Total Transaction Fee']:.2f} USD")

    # Display Trading Activity
    st.write("### Trading Activity")
    st.write(f"**Daily Trading Volume:** {analysis_results['Daily Trading Volume']:.2f} USD")
    st.write(f"**Weekly Trading Volume:** {analysis_results['Weekly Trading Volume']:.2f} USD")
    st.write(f"**Monthly Trading Volume:** {analysis_results['Monthly Trading Volume']:.2f} USD")
else:
    st.write("Please upload a CSV file to get started.")

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Function to calculate PNL and Fee analysis
def calculate_pnl_and_fee_analysis(df):
    # Normalize column names
    df.columns = df.columns.str.strip()  # Remove extra spaces
    df.columns = df.columns.str.lower()  # Convert to lowercase
    df.columns = df.columns.str.replace(' ', '_')  # Replace spaces with underscores

    # Ensure required columns exist
    required_columns = ['realized_profit', 'amount', 'fee', 'funding_fee', 'time(utc)']
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0  # Default to 0 if column is missing

    # Convert 'Time(UTC)' to datetime
    df['time(utc)'] = pd.to_datetime(df['time(utc)'])

    # Calculate Trading Costs (Commissions + Funding Fees + Liquidation Fees)
    # Assuming liquidation fees are in a column named 'liquidation_fee'
    if 'liquidation_fee' not in df.columns:
        df['liquidation_fee'] = 0  # Default to 0 if column is missing

    trading_costs = df['fee'] + df['funding_fee'] + df['liquidation_fee']

    # Adjust Realized Profit by deducting Trading Costs
    df['adjusted_realized_profit'] = df['realized_profit'] - trading_costs

    # Calculate Today's PNL
    today = datetime.utcnow().date()
    today_pnl = df[df['time(utc)'].dt.date == today]['adjusted_realized_profit'].sum()
    today_pnl_percentage = (today_pnl / df[df['time(utc)'].dt.date == today]['amount'].sum()) * 100 if df[df['time(utc)'].dt.date == today]['amount'].sum() != 0 else 0

    # Calculate 7D PNL
    last_7d = today - timedelta(days=7)
    last_7d_pnl = df[df['time(utc)'].dt.date >= last_7d]['adjusted_realized_profit'].sum()
    last_7d_pnl_percentage = (last_7d_pnl / df[df['time(utc)'].dt.date >= last_7d]['amount'].sum()) * 100 if df[df['time(utc)'].dt.date >= last_7d]['amount'].sum() != 0 else 0

    # Calculate 30D PNL
    last_30d = today - timedelta(days=30)
    last_30d_pnl = df[df['time(utc)'].dt.date >= last_30d]['adjusted_realized_profit'].sum()
    last_30d_pnl_percentage = (last_30d_pnl / df[df['time(utc)'].dt.date >= last_30d]['amount'].sum()) * 100 if df[df['time(utc)'].dt.date >= last_30d]['amount'].sum() != 0 else 0

    # Calculate Lifetime PNL
    lifetime_pnl = df['adjusted_realized_profit'].sum()
    lifetime_pnl_percentage = (lifetime_pnl / df['amount'].sum()) * 100 if df['amount'].sum() != 0 else 0

    # Return the results as a dictionary
    return {
        "Today's PNL (%)": today_pnl_percentage,
        "Today's PNL (USD)": today_pnl,
        "7D PNL (%)": last_7d_pnl_percentage,
        "7D PNL (USD)": last_7d_pnl,
        "30D PNL (%)": last_30d_pnl_percentage,
        "30D PNL (USD)": last_30d_pnl,
        "Lifetime PNL (%)": lifetime_pnl_percentage,
        "Lifetime PNL (USD)": lifetime_pnl
    }

# Streamlit App
st.title("Future Trade PNL and Fee Analysis")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file with encoding='utf-8-sig' to handle BOM
    df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
    
    # Display the uploaded data
    st.write("Uploaded Data:")
    st.write(df)
    
    # Calculate PNL and Fee Analysis
    analysis_results = calculate_pnl_and_fee_analysis(df)
    
    # Display PNL Analysis
    st.write("### PNL Analysis")
    st.write(f"**Today's PNL:** {analysis_results['Today\'s PNL (%)']:.2f}% ({analysis_results['Today\'s PNL (USD)']:.2f} USD)")
    st.write(f"**7D PNL:** {analysis_results['7D PNL (%)']:.2f}% ({analysis_results['7D PNL (USD)']:.2f} USD)")
    st.write(f"**30D PNL:** {analysis_results['30D PNL (%)']:.2f}% ({analysis_results['30D PNL (USD)']:.2f} USD)")
    st.write(f"**Lifetime PNL:** {analysis_results['Lifetime PNL (%)']:.2f}% ({analysis_results['Lifetime PNL (USD)']:.2f} USD)")
else:
    st.write("Please upload a CSV file to get started.")

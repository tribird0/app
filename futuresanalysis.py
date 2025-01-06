import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

    # Calculate Fees
    total_funding_fee = df['funding_fee'].sum()
    total_transaction_fee = df['fee'].sum()
    total_liquidation_fee = df['liquidation_fee'].sum()

    # Calculate Trading Volume
    trading_volume = df['amount'].sum()

    # Calculate Win Rate
    winning_trades = df[df['adjusted_realized_profit'] > 0].shape[0]
    total_trades = df.shape[0]
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0

    # Calculate Winning Days, Losing Days, and Breakeven Days
    df['date'] = df['time(utc)'].dt.date
    daily_pnl = df.groupby('date')['adjusted_realized_profit'].sum()
    winning_days = (daily_pnl > 0).sum()
    losing_days = (daily_pnl < 0).sum()
    breakeven_days = (daily_pnl == 0).sum()

    # Return the results as a dictionary
    return {
        "Today's PNL (%)": today_pnl_percentage,
        "Today's PNL (USD)": today_pnl,
        "7D PNL (%)": last_7d_pnl_percentage,
        "7D PNL (USD)": last_7d_pnl,
        "30D PNL (%)": last_30d_pnl_percentage,
        "30D PNL (USD)": last_30d_pnl,
        "Lifetime PNL (%)": lifetime_pnl_percentage,
        "Lifetime PNL (USD)": lifetime_pnl,
        "Total Funding Fee": total_funding_fee,
        "Total Transaction Fee": total_transaction_fee,
        "Total Liquidation Fee": total_liquidation_fee,
        "Trading Volume": trading_volume,
        "Win Rate": win_rate,
        "Winning Days": winning_days,
        "Losing Days": losing_days,
        "Breakeven Days": breakeven_days,
        "Daily PNL": daily_pnl,
        "Fee Breakdown": {
            "Funding Fee": total_funding_fee,
            "Transaction Fee": total_transaction_fee,
            "Liquidation Fee": total_liquidation_fee
        }
    }

# Streamlit App
st.title("Futures Wallet Analysis")

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
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Today's PNL", f"{analysis_results['Today\'s PNL (USD)']:.2f} USD", f"{analysis_results['Today\'s PNL (%)']:.2f}%")
    with col2:
        st.metric("7D PNL", f"{analysis_results['7D PNL (USD)']:.2f} USD", f"{analysis_results['7D PNL (%)']:.2f}%")
    with col3:
        st.metric("30D PNL", f"{analysis_results['30D PNL (USD)']:.2f} USD", f"{analysis_results['30D PNL (%)']:.2f}%")
    with col4:
        st.metric("Lifetime PNL", f"{analysis_results['Lifetime PNL (USD)']:.2f} USD", f"{analysis_results['Lifetime PNL (%)']:.2f}%")

    # Display Fee Analysis
    st.write("### Fee Analysis")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Funding Fee", f"{analysis_results['Total Funding Fee']:.2f} USD")
    with col2:
        st.metric("Total Transaction Fee", f"{analysis_results['Total Transaction Fee']:.2f} USD")
    with col3:
        st.metric("Total Liquidation Fee", f"{analysis_results['Total Liquidation Fee']:.2f} USD")

    # Display Account-Level Metrics
    st.write("### Account-Level Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Trading Volume", f"{analysis_results['Trading Volume']:.2f} USD")
    with col2:
        st.metric("Win Rate", f"{analysis_results['Win Rate']:.2f}%")
    with col3:
        st.metric("Winning Days", f"{analysis_results['Winning Days']} Days")
    with col4:
        st.metric("Losing Days", f"{analysis_results['Losing Days']} Days")

    # Visualizations
    st.write("### Visualizations")
    col1, col2 = st.columns(2)
    with col1:
        st.write("#### PNL Over Time")
        pnl_over_time = analysis_results['Daily PNL'].reset_index()
        pnl_over_time.columns = ['Date', 'PNL']
        plt.figure(figsize=(10, 6))
        plt.plot(pnl_over_time['Date'], pnl_over_time['PNL'], marker='o')
        plt.title("Daily PNL Over Time")
        plt.xlabel("Date")
        plt.ylabel("PNL (USD)")
        plt.grid(True)
        st.pyplot(plt)
    with col2:
        st.write("#### Fee Breakdown")
        fee_breakdown = pd.DataFrame(list(analysis_results['Fee Breakdown'].items()), columns=['Fee Type', 'Amount'])
        plt.figure(figsize=(6, 6))
        plt.pie(fee_breakdown['Amount'], labels=fee_breakdown['Fee Type'], autopct='%1.1f%%', startangle=140)
        plt.title("Fee Breakdown")
        st.pyplot(plt)
else:
    st.write("Please upload a CSV file to get started.")

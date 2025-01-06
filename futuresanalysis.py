import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

# Load the CSV file
uploaded_file = st.file_uploader("Upload your Binance futures trade history CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Convert relevant columns to numeric
    df['Closing PNL'] = pd.to_numeric(df['Closing PNL'], errors='coerce')
    df['Closed Vol.'] = pd.to_numeric(df['Closed Vol.'], errors='coerce')
    df['Opened'] = pd.to_datetime(df['Opened'])
    df['Closed'] = pd.to_datetime(df['Closed'])

    # Filter for closed trades
    df = df[df['Status'] == 'Closed']

    # Today's date
    today = datetime.today()

    # PNL Analysis
    today_pnl = df[df['Closed'].dt.date == today.date()]['Closing PNL'].sum()
    seven_day_pnl = df[df['Closed'] >= today - timedelta(days=7)]['Closing PNL'].sum()
    thirty_day_pnl = df[df['Closed'] >= today - timedelta(days=30)]['Closing PNL'].sum()
    lifetime_pnl = df['Closing PNL'].sum()

    # Profit and Loss Metrics
    total_profit = df[df['Closing PNL'] > 0]['Closing PNL'].sum()
    total_loss = df[df['Closing PNL'] < 0]['Closing PNL'].sum()
    net_pnl = total_profit + total_loss
    trading_volume = df['Closed Vol.'].sum()

    winning_trades = df[df['Closing PNL'] > 0].shape[0]
    losing_trades = df[df['Closing PNL'] < 0].shape[0]
    total_trades = df.shape[0]
    win_rate = (winning_trades / total_trades) * 100

    # Daily PNL
    df['Closed Date'] = df['Closed'].dt.date
    daily_pnl = df.groupby('Closed Date')['Closing PNL'].sum().reset_index()

    winning_days = daily_pnl[daily_pnl['Closing PNL'] > 0].shape[0]
    losing_days = daily_pnl[daily_pnl['Closing PNL'] < 0].shape[0]
    breakeven_days = daily_pnl[daily_pnl['Closing PNL'] == 0].shape[0]

    average_profit = total_profit / winning_trades if winning_trades > 0 else 0
    average_loss = total_loss / losing_trades if losing_trades > 0 else 0
    profit_loss_ratio = abs(average_profit / average_loss) if average_loss != 0 else 0

    # Display Results
    st.title("Binance Futures Trade Analysis")

    st.header("PNL Analysis")
    pnl_table = pd.DataFrame({
        'Metric': ["Today’s PNL", "7D PNL", "30D PNL", "Lifetime PNL"],
        'Value': [today_pnl, seven_day_pnl, thirty_day_pnl, lifetime_pnl]
    })
    st.table(pnl_table)

    st.header("Profit and Loss Metrics")
    profit_loss_table = pd.DataFrame({
        'Metric': ["Total Profit", "Total Loss", "Net Profit/Loss", "Trading Volume", "Win Rate", "Winning Days", "Losing Days", "Breakeven Days", "Average Profit", "Average Loss", "Profit/Loss Ratio"],
        'Value': [total_profit, total_loss, net_pnl, trading_volume, f"{win_rate:.2f}%", winning_days, losing_days, breakeven_days, average_profit, average_loss, profit_loss_ratio]
    })
    st.table(profit_loss_table)

else:
    st.write("Please upload a CSV file to get started.")

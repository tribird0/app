import streamlit as st
import pandas as pd

# Function to calculate PNL and Fee analysis
def calculate_pnl_and_fee_analysis(df):
    # Normalize column names
    df.columns = df.columns.str.strip()  # Remove extra spaces
    df.columns = df.columns.str.lower()  # Convert to lowercase
    df.columns = df.columns.str.replace(' ', '_')  # Replace spaces with underscores

    # Ensure required columns exist
    required_columns = ['realized_profit', 'amount', 'fee', 'funding_fee']
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0  # Default to 0 if column is missing

    # Calculate Trading Costs (Commissions + Funding Fees + Liquidation Fees)
    # Assuming liquidation fees are in a column named 'liquidation_fee'
    if 'liquidation_fee' not in df.columns:
        df['liquidation_fee'] = 0  # Default to 0 if column is missing

    trading_costs = df['fee'] + df['funding_fee'] + df['liquidation_fee']

    # Adjust Realized Profit by deducting Trading Costs
    df['adjusted_realized_profit'] = df['realized_profit'] - trading_costs

    # Calculate Total Profit (after deducting trading costs)
    total_profit = df[df['adjusted_realized_profit'] > 0]['adjusted_realized_profit'].sum()
    
    # Calculate Total Loss (after deducting trading costs)
    total_loss = df[df['adjusted_realized_profit'] < 0]['adjusted_realized_profit'].sum()
    
    # Calculate Net Profit/Loss (after deducting trading costs)
    net_pnl = total_profit + total_loss
    
    # Calculate Trading Volume
    trading_volume = df['amount'].sum()
    
    # Calculate Win Rate
    winning_trades = df[df['adjusted_realized_profit'] > 0].shape[0]
    total_trades = df.shape[0]
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
    
    # Calculate Winning Days, Losing Days, and Breakeven Days
    df['date'] = pd.to_datetime(df['time(utc)']).dt.date
    daily_pnl = df.groupby('date')['adjusted_realized_profit'].sum()
    
    winning_days = (daily_pnl > 0).sum()
    losing_days = (daily_pnl < 0).sum()
    breakeven_days = (daily_pnl == 0).sum()
    
    # Calculate Average Profit and Average Loss
    average_profit = total_profit / winning_trades if winning_trades > 0 else 0
    average_loss = total_loss / (total_trades - winning_trades) if (total_trades - winning_trades) > 0 else 0
    
    # Calculate Profit/Loss Ratio
    profit_loss_ratio = abs(average_profit / average_loss) if average_loss != 0 else 0

    # Calculate Funding Fees
    total_funding_fee = df['funding_fee'].sum()
    total_received_funding_fee = df[df['funding_fee'] > 0]['funding_fee'].sum()
    total_paid_funding_fee = df[df['funding_fee'] < 0]['funding_fee'].sum()

    # Calculate Transaction Fees
    total_transaction_fee = df['fee'].sum()

    # Calculate Liquidation Fees
    total_liquidation_fee = df['liquidation_fee'].sum()

    # Calculate Unrealized P&L (if available)
    if 'unrealized_pnl' in df.columns:
        total_unrealized_pnl = df['unrealized_pnl'].sum()
    else:
        total_unrealized_pnl = 0

    # Calculate Account-Level P&L (Transactional P&L + Fees + Unrealized P&L)
    account_level_pnl = net_pnl + total_unrealized_pnl

    # Return the results as a dictionary
    return {
        "Total Profit": total_profit,
        "Total Loss": total_loss,
        "Net Profit/Loss": net_pnl,
        "Trading Volume": trading_volume,
        "Win Rate": win_rate,
        "Winning Days": winning_days,
        "Losing Days": losing_days,
        "Breakeven Days": breakeven_days,
        "Average Profit": average_profit,
        "Average Loss": average_loss,
        "Profit/Loss Ratio": profit_loss_ratio,
        "Total Funding Fee": total_funding_fee,
        "Total Received Funding Fee": total_received_funding_fee,
        "Total Paid Funding Fee": total_paid_funding_fee,
        "Total Transaction Fee": total_transaction_fee,
        "Total Liquidation Fee": total_liquidation_fee,
        "Total Unrealized P&L": total_unrealized_pnl,
        "Account-Level P&L": account_level_pnl
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
    st.write("### Profit and Loss Analysis")
    st.write(f"**Total Profit:** {analysis_results['Total Profit']:.2f} USD")
    st.write(f"**Total Loss:** {analysis_results['Total Loss']:.2f} USD")
    st.write(f"**Net Profit/Loss:** {analysis_results['Net Profit/Loss']:.2f} USD")
    st.write(f"**Trading Volume:** {analysis_results['Trading Volume']:.2f}")
    st.write(f"**Win Rate:** {analysis_results['Win Rate']:.2f} %")
    st.write(f"**Winning Days:** {analysis_results['Winning Days']} Days")
    st.write(f"**Losing Days:** {analysis_results['Losing Days']} Days")
    st.write(f"**Breakeven Days:** {analysis_results['Breakeven Days']} Days")
    st.write(f"**Average Profit:** {analysis_results['Average Profit']:.2f} USD")
    st.write(f"**Average Loss:** {analysis_results['Average Loss']:.2f} USD")
    st.write(f"**Profit/Loss Ratio:** {analysis_results['Profit/Loss Ratio']:.2f}")

    # Display Funding and Transaction Fee Analysis
    st.write("### Funding and Transaction Fee Analysis")
    st.write(f"**Total Funding Fee:** {analysis_results['Total Funding Fee']:.2f} USD")
    st.write(f"**Total Received Funding Fee:** {analysis_results['Total Received Funding Fee']:.2f} USD")
    st.write(f"**Total Paid Funding Fee:** {analysis_results['Total Paid Funding Fee']:.2f} USD")
    st.write(f"**Total Transaction Fee:** {analysis_results['Total Transaction Fee']:.2f} USD")
    st.write(f"**Total Liquidation Fee:** {analysis_results['Total Liquidation Fee']:.2f} USD")

    # Display Account-Level P&L Analysis
    st.write("### Account-Level P&L Analysis")
    st.write(f"**Total Unrealized P&L:** {analysis_results['Total Unrealized P&L']:.2f} USD")
    st.write(f"**Account-Level P&L:** {analysis_results['Account-Level P&L']:.2f} USD")
else:
    st.write("Please upload a CSV file to get started.")

import streamlit as st
import pandas as pd

# Function to calculate PNL analysis
def calculate_pnl_analysis(df):
    # Normalize column names
    df.columns = df.columns.str.strip()  # Remove extra spaces
    df.columns = df.columns.str.lower()  # Convert to lowercase
    df.columns = df.columns.str.replace(' ', '_')  # Replace spaces with underscores

    # Calculate Total Profit
    total_profit = df[df['realized_profit'] > 0]['realized_profit'].sum()
    
    # Calculate Total Loss
    total_loss = df[df['realized_profit'] < 0]['realized_profit'].sum()
    
    # Calculate Net Profit/Loss
    net_pnl = total_profit + total_loss
    
    # Calculate Trading Volume
    trading_volume = df['amount'].sum()
    
    # Calculate Win Rate
    winning_trades = df[df['realized_profit'] > 0].shape[0]
    total_trades = df.shape[0]
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
    
    # Calculate Winning Days, Losing Days, and Breakeven Days
    df['date'] = pd.to_datetime(df['time(utc)']).dt.date
    daily_pnl = df.groupby('date')['realized_profit'].sum()
    
    winning_days = (daily_pnl > 0).sum()
    losing_days = (daily_pnl < 0).sum()
    breakeven_days = (daily_pnl == 0).sum()
    
    # Calculate Average Profit and Average Loss
    average_profit = total_profit / winning_trades if winning_trades > 0 else 0
    average_loss = total_loss / (total_trades - winning_trades) if (total_trades - winning_trades) > 0 else 0
    
    # Calculate Profit/Loss Ratio
    profit_loss_ratio = abs(average_profit / average_loss) if average_loss != 0 else 0
    
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
        "Profit/Loss Ratio": profit_loss_ratio
    }

# Streamlit App
st.title("Future Trade PNL Analysis")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file with encoding='utf-8-sig' to handle BOM
    df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
    
    # Display the uploaded data
    st.write("Uploaded Data:")
    st.write(df)
    
    # Calculate PNL Analysis
    pnl_analysis = calculate_pnl_analysis(df)
    
    # Display PNL Analysis
    st.write("### Profit and Loss Analysis")
    st.write(f"**Total Profit:** {pnl_analysis['Total Profit']:.2f} USD")
    st.write(f"**Total Loss:** {pnl_analysis['Total Loss']:.2f} USD")
    st.write(f"**Net Profit/Loss:** {pnl_analysis['Net Profit/Loss']:.2f} USD")
    st.write(f"**Trading Volume:** {pnl_analysis['Trading Volume']:.2f}")
    st.write(f"**Win Rate:** {pnl_analysis['Win Rate']:.2f} %")
    st.write(f"**Winning Days:** {pnl_analysis['Winning Days']} Days")
    st.write(f"**Losing Days:** {pnl_analysis['Losing Days']} Days")
    st.write(f"**Breakeven Days:** {pnl_analysis['Breakeven Days']} Days")
    st.write(f"**Average Profit:** {pnl_analysis['Average Profit']:.2f} USD")
    st.write(f"**Average Loss:** {pnl_analysis['Average Loss']:.2f} USD")
    st.write(f"**Profit/Loss Ratio:** {pnl_analysis['Profit/Loss Ratio']:.2f}")
else:
    st.write("Please upload a CSV file to get started.")

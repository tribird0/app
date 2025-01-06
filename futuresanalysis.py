import streamlit as st

# Title and description
st.title("Binance Futures Calculator")
st.write("Calculate Liquidation Price and PNL for your Binance Futures positions.")

# Input widgets
st.subheader("Input Parameters")

# Position type
position = st.selectbox("Position", ["Long", "Short"])

# Margin mode
margin_mode = st.selectbox("Margin Mode", ["Isolated", "Cross"])

# Leverage
leverage = st.number_input("Leverage", min_value=1.0, value=12.0)

# Wallet balance (only for Cross margin)
if margin_mode == "Cross":
    wallet_balance = st.number_input("Wallet Balance", min_value=0.0, value=1000.0)
else:
    wallet_balance = None

# Contract type
contract_type = st.selectbox("Contract Type", ["USDS-M Futures", "COIN-M Futures"])

# Entry and Exit prices
entry_price = st.number_input("Entry Price", min_value=0.0, value=50000.0)
exit_price = st.number_input("Exit Price", min_value=0.0, value=55000.0)

# Maintenance margin rate
maintenance_margin_rate = st.number_input("Maintenance Margin Rate (%)", min_value=0.0, value=0.40) / 100

# Maintenance amount (optional)
maintenance_amount = st.number_input("Maintenance Amount (optional)", min_value=0.0, value=0.0)

# Calculation functions
def calculate_liquidation_price(position, entry_price, leverage, maintenance_margin_rate, maintenance_amount=None):
    if maintenance_amount:
        if position == "Long":
            liquidation_price = (entry_price * (1 - maintenance_margin_rate)) / (1 + (maintenance_amount / entry_price))
        else:
            liquidation_price = (entry_price * (1 + maintenance_margin_rate)) / (1 - (maintenance_amount / entry_price))
    else:
        if position == "Long":
            liquidation_price = (entry_price * (1 - maintenance_margin_rate)) / (1 + (maintenance_margin_rate * (leverage - 1)))
        else:
            liquidation_price = (entry_price * (1 + maintenance_margin_rate)) / (1 - (maintenance_margin_rate * (leverage - 1)))
    return liquidation_price

def calculate_pnl(position, contract_type, entry_price, exit_price, leverage):
    if contract_type == "USDS-M Futures":
        if position == "Long":
            pnl = ((exit_price / entry_price) - 1) * leverage
        else:
            pnl = (1 - (entry_price / exit_price)) * leverage
    else:
        if position == "Long":
            pnl = ((exit_price - entry_price) / entry_price) * leverage
        else:
            pnl = ((entry_price - exit_price) / entry_price) * leverage
    return pnl

# Calculate and display results
st.subheader("Results")

try:
    liquidation_price = calculate_liquidation_price(position, entry_price, leverage, maintenance_margin_rate, maintenance_amount)
    pnl = calculate_pnl(position, contract_type, entry_price, exit_price, leverage)
    
    st.write(f"Liquidation Price: **{liquidation_price:.2f}**")
    st.write(f"PNL: **{pnl:.2%}**")
except ZeroDivisionError:
    st.write("Error: Division by zero occurred. Please check your inputs.")
except:
    st.write("An error occurred. Please verify your input values.")

# Additional notes
st.write("Note: PNL is displayed as a percentage for simplicity.")
st.write("Disclaimer: This calculator is for educational purposes only.")

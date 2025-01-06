import streamlit as st
import pandas as pd

# Set page title
st.title('Crypto Future Trading Realized PnL Calculator')

# Introduction
st.write('Upload your trades data in CSV format to calculate your realized profit and loss.')

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    trades = pd.read_csv(uploaded_file)
    
    # Ensure the necessary columns are present
    required_columns = ['Position', 'Entry Price', 'Exit Price', 'Quantity', 'Fees (%)']
    if not all(col in trades.columns for col in required_columns):
        st.error("The CSV file is missing some required columns.")
    else:
        # Calculate Realized PnL
        pnl_list = []
        total_pnl = 0.0

        for index, row in trades.iterrows():
            position = row['Position']
            entry_price = row['Entry Price']
            exit_price = row['Exit Price']
            quantity = row['Quantity']
            fees_percent = row['Fees (%)']
            
            if position == 'Long':
                pnl = (exit_price - entry_price) * quantity
            else:  # Short
                pnl = (entry_price - exit_price) * quantity
            
            fees_amount = (entry_price * quantity) * (fees_percent / 100)
            pnl -= fees_amount
            pnl_list.append(pnl)
            total_pnl += pnl

        # Add PnL to the trades DataFrame
        trades['PnL'] = pnl_list

        # Display the results
        st.subheader('Trades Details')
        st.write(trades)
        
        st.subheader('Total Realized PnL')
        st.write(f'**{total_pnl:.2f}**')
        
        # Optional: Add a simple chart
        st.subheader('PnL Distribution')
        st.bar_chart(trades['PnL'])
else:
    st.info('Please upload a CSV file containing your trades data.')

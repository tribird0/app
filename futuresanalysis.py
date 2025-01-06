import pandas as pd
import streamlit as st

# Function to calculate PnL for each trade
def calculate_pnl(row):
    if row['Position'] == 'Long':
        pnl = (row['Exit Price'] - row['Entry Price']) * row['Quantity']
    elif row['Position'] == 'Short':
        pnl = (row['Entry Price'] - row['Exit Price']) * row['Quantity']
    else:
        pnl = 0  # Unknown position type
    fees = (row['Entry Price'] * row['Quantity']) * (row['Fees (%)'] / 100)
    pnl -= fees
    return pnl

# Main function to calculate total PnL
def main():
    st.title('Binance Futures PnL Calculator')

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload your trades CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)

        # Ensure the necessary columns are present
        required_columns = ['Position', 'Entry Price', 'Exit Price', 'Quantity', 'Fees (%)']
        if not all(col in df.columns for col in required_columns):
            st.error("The CSV file is missing some required columns.")
            return

        # Filter for Binance futures trades (if necessary)
        # Assuming there's a 'Platform' column indicating the exchange
        df_binance = df[df['Platform'] == 'Binance']

        # Apply the PnL calculation function
        df_binance['PnL'] = df_binance.apply(calculate_pnl, axis=1)

        # Calculate total profit/loss
        total_pnl = df_binance['PnL'].sum()

        # Display the result
        st.subheader('Total Profit/Loss')
        st.write(f"**{total_pnl:.2f}**")

        # Display PnL statistics
        st.subheader('PnL Statistics')
        st.write(df_binance['PnL'].describe())

        # Plot PnL distribution
        st.subheader('PnL Distribution')
        fig, ax = plt.subplots()
        ax.hist(df_binance['PnL'], bins=20, edgecolor='black')
        ax.set_title('Distribution of Profit and Loss')
        ax.set_xlabel('PnL')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

# Run the app
if __name__ == '__main__':
    main()

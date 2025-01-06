import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title('Futures Trade PNL Analysis')

# Upload CSV file
uploaded_file = st.file_uploader("Upload your trade data CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Display raw data
    st.subheader('Raw Data')
    st.dataframe(df)
    
    # Calculate PNL
    df['PNL'] = (df['Exit Price'] - df['Entry Price']) * df['Quantity']
    
    # Display Total PNL
    st.subheader('Total PNL')
    total_pnl = df['PNL'].sum()
    st.write(f'${total_pnl:.2f}')
    
    # PNL Distribution
    st.subheader('PNL Distribution')
    fig, ax = plt.subplots()
    df['PNL'].hist(ax=ax, bins=20)
    ax.set_xlabel('Profit and Loss')
    ax.set_ylabel('Number of Trades')
    st.pyplot(fig)
    
    # Cumulative PNL over time
    if 'Trade Date' in df.columns:
        df['Trade Date'] = pd.to_datetime(df['Trade Date'])
        df.sort_values('Trade Date', inplace=True)
        df['Cumulative PNL'] = df['PNL'].cumsum()
        
        st.subheader('Cumulative PNL Over Time')
        fig, ax = plt.subplots()
        df.plot(x='Trade Date', y='Cumulative PNL', ax=ax)
        ax.set_xlabel('Date')
        ax.set_ylabel('Cumulative PNL')
        st.pyplot(fig)
    else:
        st.warning("No 'Trade Date' column found for time series analysis.")
    
    # Filter trades by PNL
    st.subheader('Filter Trades by PNL')
    pnl_min, pnl_max = st.slider('Select PNL range', 
                                 float(df['PNL'].min()), float(df['PNL'].max()), 
                                 (float(df['PNL'].min()), float(df['PNL'].max())))
    filtered_df = df[(df['PNL'] >= pnl_min) & (df['PNL'] <= pnl_max)]
    st.dataframe(filtered_df)
    
    # PNL Statistics
    st.subheader('PNL Statistics')
    st.write(df['PNL'].describe())
else:
    st.info('Please upload a CSV file.')

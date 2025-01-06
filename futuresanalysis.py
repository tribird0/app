import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Futures PNL Analysis", layout="wide")

# Title and subtitle
st.title("Futures Trade PNL Analysis")
st.subheader("Analyze your trading performance with this interactive tool.")

# Instructions and sample CSV download
st.markdown("[Download Sample CSV](sample_trades.csv)")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your trade data CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['Trade Time'] = pd.to_datetime(df['Trade Time'])
    df['PNL'] = df.apply(
        lambda row: (row['Exit Price'] - row['Entry Price']) * row['Quantity'] * row['Leverage']
        if row['Position Side'] == 'Long'
        else (row['Entry Price'] - row['Exit Price']) * row['Quantity'] * row['Leverage'],
        axis=1
    )
    df.sort_values('Trade Time', inplace=True)
    df['Cumulative PNL'] = df['PNL'].cumsum()
    
    # Sidebar filters
    st.sidebar.header('Filters')
    start_date, end_date = st.sidebar.date_input('Select Date Range', (df['Trade Time'].min(), df['Trade Time'].max()))
    symbol = st.sidebar.selectbox('Select Symbol', df['Symbol'].unique())
    position_side = st.sidebar.radio('Select Position Side', ['All', 'Long', 'Short'])
    
    # Apply filters
    filtered_df = df[(df['Trade Time'] >= start_date) & (df['Trade Time'] <= end_date)]
    filtered_df = filtered_df[filtered_df['Symbol'] == symbol]
    if position_side != 'All':
        filtered_df = filtered_df[filtered_df['Position Side'] == position_side]
    
    # Visualizations
    st.subheader('PNL Distribution')
    fig_histogram = px.histogram(filtered_df, x='PNL', nbins=30, title='PNL Distribution')
    st.plotly_chart(fig_histogram)
    
    st.subheader('Cumulative PNL Over Time')
    fig_cumulative = px.line(filtered_df, x='Trade Time', y='Cumulative PNL', title='Cumulative PNL Over Time')
    st.plotly_chart(fig_cumulative)
    
    st.subheader('Profit vs. Loss')
    profit = filtered_df[filtered_df['PNL'] > 0]['PNL'].sum()
    loss = filtered_df[filtered_df['PNL'] < 0]['PNL'].sum()
    fig_pie = px.pie(values=[profit, loss], names=['Profit', 'Loss'], title='Profit vs. Loss')
    st.plotly_chart(fig_pie)
    
    # Key Metrics
    st.subheader('Key Metrics')
    total_pnl = filtered_df['PNL'].sum()
    average_pnl = filtered_df['PNL'].mean()
    win_loss_ratio = len(filtered_df[filtered_df['PNL'] > 0]) / len(filtered_df[filtered_df['PNL'] < 0]) if len(filtered_df[filtered_df['PNL'] < 0]) > 0 else float('inf')
    st.write(f'Total PNL: ${total_pnl:.2f}')
    st.write(f'Average PNL: ${average_pnl:.2f}')
    st.write(f'Win/Loss Ratio: {win_loss_ratio:.2f}')
    
    # Trade Details
    st.subheader('Trade Details')
    st.dataframe(filtered_df)
else:
    st.info('Please upload a CSV file.')

import streamlit as st
import pandas as pd
import os

# Function to filter DataFrame by keyword and save specific columns
def filter_and_save(df, keyword, filename, columns, output_dir):
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(keyword).any(), axis=1)]
    filtered_df = filtered_df.iloc[:, columns]
    filtered_df.to_csv(os.path.join(output_dir, filename), index=False)

# Function to sort a CSV file by the second column and save it
def sort_and_save(df, sorted_filename, key=1):
    df_sorted = df.sort_values(by=df.columns[key])
    return df_sorted

# Function to separate negative and positive values
def separate_neg_pos(df, neg_file, pos_file, output_dir):
    df['Value'] = pd.to_numeric(df.iloc[:, 1], errors='coerce')
    df_neg = df[df['Value'] < 0]
    df_pos = df[df['Value'] >= 0]
    df_neg.to_csv(os.path.join(output_dir, neg_file), index=False)
    df_pos.to_csv(os.path.join(output_dir, pos_file), index=False)
    return df_neg, df_pos

# Function to get top values
def get_top_values(df, top_n, ascending=False):
    df['Value'] = pd.to_numeric(df.iloc[:, 1], errors='coerce')
    top_df = df.nlargest(top_n, 'Value') if not ascending else df.nsmallest(top_n, 'Value')
    return top_df

# Main Streamlit app
def main():
    st.title('Crypto Trading Analysis App')
    st.write('Upload your CSV file to analyze trading data.')

    # Upload CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Create a temporary directory to store output files
        output_dir = 'op'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Filter and save data for each keyword
        keywords = [
            ('REALIZED_PNL', 'pnl.csv', [2, 4]),
            ('COMMISSION', 'commision.csv', [2, 4]),
            ('INSURANCE_CLEAR', 'liq.csv', [2, 4]),
            ('FUNDING_FEE', 'fun.csv', [2, 4])
        ]

        for keyword, filename, columns in keywords:
            filter_and_save(df, keyword, filename, columns, output_dir)

        # Read filtered CSV files
        try:
            df_pnl = pd.read_csv(os.path.join(output_dir, 'pnl.csv'))
            df_comm = pd.read_csv(os.path.join(output_dir, 'commision.csv'))
            df_liq = pd.read_csv(os.path.join(output_dir, 'liq.csv'))
            df_fun = pd.read_csv(os.path.join(output_dir, 'fun.csv'))
        except Exception as e:
            st.error(f"Error reading filtered CSV files: {e}")
            return

        # Sort the CSV files
        df_pnl_sorted = sort_and_save(df_pnl, 'sorted-pnl.csv')
        df_comm_sorted = sort_and_save(df_comm, 'sorted-commision.csv')
        df_liq_sorted = sort_and_save(df_liq, 'sorted-liq.csv')
        df_fun_sorted = sort_and_save(df_fun, 'sorted-fun.csv')

        # Separate negative and positive values
        df_loss, df_profit = separate_neg_pos(df_pnl_sorted, 'loss.csv', 'profit.csv', output_dir)
        df_negative_comm, df_positive_comm = separate_neg_pos(df_comm_sorted, 'negative-commision.csv', 'positive-commision.csv', output_dir)
        df_negative_fun, df_positive_fun = separate_neg_pos(df_fun_sorted, 'negative-fun.csv', 'positive-fun.csv', output_dir)

        # Get top values
        top_10_loss = get_top_values(df_loss, 10, ascending=True)
        top_10_profit = get_top_values(df_profit, 10)
        top_10_liq = get_top_values(df_liq_sorted, 10, ascending=True)
        top_5_negative_comm = get_top_values(df_negative_comm, 5, ascending=True)
        top_5_positive_comm = get_top_values(df_positive_comm, 5)
        top_5_negative_fun = get_top_values(df_negative_fun, 5, ascending=True)
        top_5_positive_fun = get_top_values(df_positive_fun, 5)

        # Calculate totals
        pr = df_profit['Value'].sum()
        los = df_loss['Value'].sum()
        liq = df_liq['Value'].sum()
        fee = df_comm['Value'].sum()
        fun = df_fun['Value'].sum()
        to_los = los + fee + liq + fun
        tot = pr + los + fee + liq + fun

        # Display results
        st.header('Analysis Results')

        st.subheader('Total Profit')
        st.write(f"**{pr:.2f}**")

        st.subheader('Total Loss')
        st.write(f"**{los:.2f}**")

        st.subheader('Total Liquidation')
        st.write(f"**{liq:.2f}**")

        st.subheader('Total Commission')
        st.write(f"**{fee:.2f}**")

        st.subheader('Total Funding Fee')
        st.write(f"**{fun:.2f}**")

        st.subheader('Total Loss Including Fees & Liquidation & Commission')
        st.write(f"**{to_los:.2f}**")

        st.subheader('Capital Lost')
        st.write(f"**{tot:.2f}**")

        # Display top values
        st.subheader('Top 10 Loss')
        st.dataframe(top_10_loss)

        st.subheader('Top 10 Profit')
        st.dataframe(top_10_profit)

        st.subheader('Top 10 Loss Due to Liquidation')
        st.dataframe(top_10_liq)

        st.subheader('Top 5 Negative Commission')
        st.dataframe(top_5_negative_comm)

        st.subheader('Top 5 Positive Commission')
        st.dataframe(top_5_positive_comm)

        st.subheader('Top 5 Negative Funding Fees')
        st.dataframe(top_5_negative_fun)

        st.subheader('Top 5 Positive Funding Fees')
        st.dataframe(top_5_positive_fun)

# Run the app
if __name__ == '__main__':
    main()

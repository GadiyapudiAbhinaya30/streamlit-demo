import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Sales Data Analyzer", layout="wide")

st.title("📈 Sales Data Analyzer")
st.write("Upload a CSV file to analyze your sales data!")

# Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the data
    df = pd.read_csv(uploaded_file)
    st.subheader("🔍 Raw Data")
    st.dataframe(df)

    # Shape and Columns
    st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    st.write("Columns:", list(df.columns))

    # Basic statistics using NumPy
    st.subheader(" Statistical Summary")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    if numeric_cols:
        stats = df[numeric_cols].agg(["mean", "min", "max", "std", "sum"])
        st.dataframe(stats)
    else:
        st.warning("No numeric columns found in the dataset.")

    # Column filtering
    st.subheader(" Filter by Column")
    column_to_filter = st.selectbox("Select column to filter", df.columns)
    unique_vals = df[column_to_filter].dropna().unique()

    selected_val = st.selectbox("Select value", unique_vals)
    filtered_df = df[df[column_to_filter] == selected_val]
    st.dataframe(filtered_df)

    # Time Series chart if 'Date' and 'Revenue' columns exist
    if 'Date' in df.columns and 'Revenue' in df.columns:
        try:
            df['Date'] = pd.to_datetime(df['Date'])
            revenue_over_time = df.groupby('Date')['Revenue'].sum()
            st.subheader(" Revenue Over Time")
            st.line_chart(revenue_over_time)
        except Exception as e:
            st.warning("Couldn't plot revenue over time. Error: " + str(e))

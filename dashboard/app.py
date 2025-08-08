# Streamlit dashboard app for vehicle registration data (investor-focused)
import streamlit as st
import pandas as pd
from dashboard.data_loader import load_data, preprocess_data, filter_data
from dashboard.metrics import calculate_yoy_growth, calculate_qoq_growth

st.set_page_config(page_title="Vehicle Registration Dashboard", layout="wide")
st.title("Vehicle Registration Dashboard (Investor View)")

# Sidebar: Data upload and filters
st.sidebar.header("Data & Filters")
data_file = st.sidebar.file_uploader("Upload Vahan data (CSV/Excel)", type=["csv", "xlsx"])

if data_file:
    df = load_data(data_file)
    df = preprocess_data(df)
    # Sidebar filters
    min_date, max_date = df['date'].min(), df['date'].max()
    start_date, end_date = st.sidebar.date_input("Date range", [min_date, max_date])
    categories = st.sidebar.multiselect("Vehicle Category", options=sorted(df['vehicle_category'].unique()))
    manufacturers = st.sidebar.multiselect("Manufacturer", options=sorted(df['manufacturer'].unique()))
    filtered_df = filter_data(df, str(start_date), str(end_date), categories, manufacturers)
    st.write(f"### Showing {len(filtered_df)} records")
    # Metrics
    st.subheader("YoY Growth by Category")
    yoy_cat = calculate_yoy_growth(filtered_df, 'vehicle_category')
    st.dataframe(yoy_cat)
    st.subheader("QoQ Growth by Category")
    qoq_cat = calculate_qoq_growth(filtered_df, 'vehicle_category')
    st.dataframe(qoq_cat)
    st.subheader("YoY Growth by Manufacturer")
    yoy_manu = calculate_yoy_growth(filtered_df, 'manufacturer')
    st.dataframe(yoy_manu)
    st.subheader("QoQ Growth by Manufacturer")
    qoq_manu = calculate_qoq_growth(filtered_df, 'manufacturer')
    st.dataframe(qoq_manu)
    # Graphs
    st.subheader("Trends & % Change")
    st.line_chart(yoy_cat.pivot(index='year', columns='vehicle_category', values='yoy_growth'))
    st.line_chart(qoq_cat.pivot(index='quarter', columns='vehicle_category', values='qoq_growth'))
    st.line_chart(yoy_manu.pivot(index='year', columns='manufacturer', values='yoy_growth'))
    st.line_chart(qoq_manu.pivot(index='quarter', columns='manufacturer', values='qoq_growth'))
else:
    st.info("Please upload a Vahan data file to begin.")

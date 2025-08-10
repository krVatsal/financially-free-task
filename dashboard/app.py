# Streamlit dashboard app for vehicle registration data (Investor Professional Edition)
import streamlit as st
import pandas as pd
import numpy as np
import os
from db_utils import create_connection, load_csv_to_sqlite
import plotly.express as px

st.set_page_config(page_title="Vehicle Registration Investor Dashboard", layout="wide")
st.title("Vehicle Registration Dashboard (Investor Edition)")
st.markdown("""
<div style='font-size:18px; color:#444;'>
A professional, investor-focused dashboard for India's vehicle registration trends. Use the controls to analyze Four, Three, and (soon) Two Wheeler data for growth, resilience, and market opportunities.
</div>
""", unsafe_allow_html=True)

# Paths
base = os.path.dirname(__file__)
db_path = os.path.join(base, 'vehicle_data.db')

# Ensure DB is loaded
if not os.path.exists(db_path):
    # Load all available CSVs
    for fname, tname in [
        ("four_wheeler_data.csv", "four_wheeler"),
        ("three_wheeler_data.csv", "three_wheeler"),
        ("two_wheeler_data.csv", "two_wheeler")
    ]:
        fpath = os.path.join(base, fname)
        if os.path.exists(fpath):
            load_csv_to_sqlite(fpath, db_path, tname)


# Vehicle type selector
vehicle_type = st.sidebar.selectbox("Select Vehicle Type", ["Four Wheeler", "Three Wheeler", "Two Wheeler"], index=0)
table_map = {
    "Four Wheeler": {
        "table": "four_wheeler",
        "cols": ['4WIC', 'LMV', 'MMV', 'HMV', 'TOTAL'],
        "pivot_values": ['4WIC', 'LMV', 'MMV', 'HMV', 'TOTAL']
    },
    "Three Wheeler": {
        "table": "three_wheeler",
        "cols": ['3WN', '3WT', 'TOTAL'],
        "pivot_values": ['3WN', '3WT', 'TOTAL']
    },
    "Two Wheeler": {
        "table": "two_wheeler",
        "cols": ['2WIC', '2WN', '2WT', 'TOTAL'],
        "pivot_values": ['2WIC', '2WN', '2WT', 'TOTAL']
    }
}

meta = table_map[vehicle_type]
conn = create_connection(db_path)

# Get all years and vehicle classes
years_all = pd.read_sql_query(f"SELECT DISTINCT Year FROM {meta['table']}", conn)['Year'].tolist()
vehicle_classes = pd.read_sql_query(f"SELECT DISTINCT [Vehicle Class] FROM {meta['table']}", conn)['Vehicle Class'].tolist()

# Separate 'Till date' from years
years = [y for y in years_all if str(y).lower() != 'till date']
has_till_date = any(str(y).lower() == 'till date' for y in years_all)

selected_years = st.sidebar.multiselect("Select Year(s)", options=years + (["Till date"] if has_till_date else []), default=years)
selected_classes = st.sidebar.multiselect("Select Vehicle Class(es)", options=vehicle_classes, default=vehicle_classes)

if not selected_years or not selected_classes:
    st.info("Please select at least one year and one vehicle class to view data and insights.")
    st.stop()

# Main query
query = f"SELECT * FROM {meta['table']} WHERE Year IN ({','.join(['?']*len(selected_years))}) AND [Vehicle Class] IN ({','.join(['?']*len(selected_classes))})"
params = selected_years + selected_classes
df = pd.read_sql_query(query, conn, params=params)
conn.close()

# Separate out Till date row(s) for special handling
df_till = df[df['Year'].astype(str).str.lower() == 'till date']
df = df[df['Year'].astype(str).str.lower() != 'till date']

# Data cleaning for professional display
def format_number(x):
    if pd.isna(x):
        return x
    try:
        return int(str(x).replace(",", ""))
    except:
        return x
for col in meta['cols']:
    if col in df.columns:
        df[col] = df[col].apply(format_number)


# Show data
tab1, tab2 = st.tabs(["Data Table", "Investor Metrics & Visuals"])
with tab1:
    st.markdown(f"### 📊 Filtered Data Table: {vehicle_type}")
    st.dataframe(df, use_container_width=True)
    if not df_till.empty:
        st.markdown("#### 🟡 Cumulative (Till date)")
        st.dataframe(df_till, use_container_width=True)
    st.download_button(f"Download Filtered Data as CSV", pd.concat([df, df_till]).to_csv(index=False), f"filtered_{vehicle_type.lower().replace(' ', '_')}.csv")

with tab2:
    st.markdown(f"## 📈 Key Investor Metrics: {vehicle_type}")
    # Total registrations trend (exclude Till date)
    reg_by_year = df.groupby('Year')['TOTAL'].sum().reset_index()
    fig1 = px.line(reg_by_year, x='Year', y='TOTAL', markers=True, title=f"Total {vehicle_type} Registrations by Year", labels={'TOTAL':'Total Registrations'})
    fig1.update_traces(line_color='#0072B5', marker_color='#0072B5')
    st.plotly_chart(fig1, use_container_width=True)

    # Show Till date as cumulative metric if present
    if not df_till.empty:
        till_total = df_till['TOTAL'].sum()
        st.metric("Cumulative (Till date) Total Registrations", f"{till_total:,}")

    # YoY Growth (exclude Till date)
    reg_by_year['YoY % Growth'] = reg_by_year['TOTAL'].pct_change().mul(100).round(2)
    fig2 = px.bar(reg_by_year, x='Year', y='YoY % Growth', title="Year-over-Year (YoY) Growth (%)", color='YoY % Growth', color_continuous_scale='Blues')
    st.plotly_chart(fig2, use_container_width=True)

    # Vehicle class share (exclude Till date)
    reg_by_class = df.groupby('Vehicle Class')['TOTAL'].sum().reset_index()
    fig3 = px.pie(reg_by_class, names='Vehicle Class', values='TOTAL', title="Share by Vehicle Class")
    st.plotly_chart(fig3, use_container_width=True)

    # Top 5 years for total registrations (exclude Till date)
    st.markdown("**Top 5 Years for Total Registrations**")
    top5 = reg_by_year.sort_values('TOTAL', ascending=False).head(5)
    st.table(top5)

    # Best performing vehicle class by year (exclude Till date)
    st.markdown("**Best Performing Vehicle Class Each Year**")
    best_class = df.loc[df.groupby('Year')['TOTAL'].idxmax()][['Year', 'Vehicle Class', 'TOTAL']]
    st.table(best_class)

    # Custom Pivot Table (exclude Till date)
    st.markdown("---")
    st.markdown("## 🧮 Custom Pivot Table & Advanced Analysis")
    pivot_index = st.multiselect("Pivot Index (rows)", options=['Year', 'Vehicle Class'], default=['Year'], key='pivot_index')
    pivot_columns = st.multiselect("Pivot Columns", options=['Vehicle Class'], default=[], key='pivot_columns')
    pivot_values = st.multiselect("Pivot Values", options=meta['pivot_values'], default=['TOTAL'], key='pivot_values')
    if pivot_index:
        pivot = pd.pivot_table(df, index=pivot_index, columns=pivot_columns, values=pivot_values, aggfunc='sum', fill_value=0)
        st.dataframe(pivot, use_container_width=True)

    # Highlight positive trends (exclude Till date)
    st.markdown("---")
    st.markdown("## 🟢 Positive Trends & Resilience")
    pos_growth = reg_by_year[reg_by_year['YoY % Growth'] > 0].sort_values('YoY % Growth', ascending=False)
    if not pos_growth.empty:
        st.markdown(f"**Years with highest positive YoY growth:**")
        st.table(pos_growth[['Year', 'YoY % Growth']].head(5))
    class_growth = df.groupby(['Vehicle Class', 'Year'])['TOTAL'].sum().reset_index()
    class_growth['YoY'] = class_growth.groupby('Vehicle Class')['TOTAL'].pct_change().mul(100).round(2)
    consistent = class_growth.groupby('Vehicle Class').filter(lambda x: (x['YoY'] > 0).sum() >= 3)
    if not consistent.empty:
        st.markdown("**Vehicle classes with 3+ years of positive YoY growth:**")
        st.dataframe(consistent[['Vehicle Class', 'Year', 'YoY']])

    # Additional investor metrics (exclude Till date)
    st.markdown("---")
    st.markdown("## 🏆 Additional Investor Metrics")
    # CAGR
    if len(reg_by_year) > 1:
        start, end = reg_by_year.iloc[0]['TOTAL'], reg_by_year.iloc[-1]['TOTAL']
        n = len(reg_by_year) - 1
        cagr = ((end / start) ** (1/n) - 1) * 100 if start > 0 else np.nan
        st.metric("CAGR (Compound Annual Growth Rate)", f"{cagr:.2f}%")
    # Volatility
    volatility = reg_by_year['TOTAL'].pct_change().std() * 100
    st.metric("Volatility (Std Dev of YoY Growth)", f"{volatility:.2f}%")
    # Best/Worst year
    if not reg_by_year.empty:
        best_year = reg_by_year.loc[reg_by_year['TOTAL'].idxmax()]['Year']
        worst_year = reg_by_year.loc[reg_by_year['TOTAL'].idxmin()]['Year']
        st.metric("Best Year (Total)", best_year)
        st.metric("Worst Year (Total)", worst_year)

st.caption("Data source: Vahan Dashboard (manual extraction). Dashboard by Investor Analytics.")

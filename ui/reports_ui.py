# ui/reports_ui.py

import streamlit as st
import pandas as pd
from utils import db_utils

def run():
    """
    The main function to run the Reports page.
    """
    st.title("📊 Sales Reports & Analytics")
    st.markdown("---")

    # Fetch all order data using our utility function
    all_orders_data = db_utils.get_all_orders()

    if not all_orders_data:
        st.warning("No sales data found. Please generate some bills first.")
        return

    # Convert the data into a pandas DataFrame for easy analysis
    df = pd.DataFrame(all_orders_data)
    df['order_date'] = pd.to_datetime(df['order_date'])

    # --- Key Performance Indicators (KPIs) ---
    total_revenue = df['grand_total'].unique().sum()
    total_orders = df['order_id'].nunique()
    
    st.header("📈 Key Metrics")
    kpi1, kpi2 = st.columns(2)
    with kpi1:
        st.metric(label="Total Revenue", value=f"₹{total_revenue:.2f}")
    with kpi2:
        st.metric(label="Total Orders", value=total_orders)
    
    st.markdown("---")

    # --- Most Sold Items Report ---
    st.header("🍕 Most Sold Items")
    most_sold = df.groupby('item_name')['quantity'].sum().sort_values(ascending=False).reset_index()
    st.dataframe(most_sold)

    # --- Sales Over Time Chart ---
    st.header("📅 Daily Sales")
    daily_sales = df.set_index('order_date').resample('D')['grand_total'].sum()
    st.bar_chart(daily_sales)

    # --- Raw Data View ---
    with st.expander("View Raw Sales Data"):
        st.dataframe(pd.DataFrame(db_utils.get_order_summary()))
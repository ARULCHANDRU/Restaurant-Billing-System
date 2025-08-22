# app.py

import streamlit as st
from ui import main_ui, reports_ui
from utils import db_utils

# --- INITIAL SETUP ---
db_utils.init_db()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Billing", "Reports"])

# --- PAGE ROUTING ---
if page == "Billing":
    main_ui.run()
elif page == "Reports":
    reports_ui.run()
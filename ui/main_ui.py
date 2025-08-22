# ui/main_ui.py

import streamlit as st
import pandas as pd
from utils import db_utils, calculator

# --- Helper functions ---
def add_item_to_order(item):
    for order_item in st.session_state.current_order:
        if order_item['item_id'] == item['item_id']:
            order_item['quantity'] += 1
            return
    new_item = item.copy()
    new_item['quantity'] = 1
    st.session_state.current_order.append(new_item)

def remove_item_from_order(item_id):
    st.session_state.current_order = [
        item for item in st.session_state.current_order if item['item_id'] != item_id
    ]

def run():
    # --- PAGE CONFIGURATION ---
    st.set_page_config(page_title="Restaurant Billing", page_icon="🍽️", layout="wide")
    st.title("🍽️ Restaurant Billing System")

    # --- CHANGE #1: Display Success Message on Rerun ---
    # Check if a success message needs to be shown from the previous run.
    if st.session_state.get('show_success'):
        st.success(st.session_state.get('success_message', 'Success!'))
        st.balloons()
        # Clear the flag so it doesn't show again on the next refresh.
        del st.session_state['show_success']
        del st.session_state['success_message']

    st.markdown("---")

    # --- SESSION STATE INITIALIZATION ---
    if 'current_order' not in st.session_state:
        st.session_state.current_order = []

    # --- LAYOUT ---
    menu_col, bill_col = st.columns([2, 1])

    # --- MENU COLUMN (Left Side) ---
    with menu_col:
        st.header("📜 Menu")
        menu_items = db_utils.get_menu()
        if not menu_items:
            st.warning("No menu items found. Please populate the menu.")
        else:
            categories = pd.DataFrame(menu_items)['category'].unique()
            for category in categories:
                st.subheader(f"- {category} -")
                cat_col1, cat_col2, cat_col3 = st.columns([2, 1, 1])
                category_items = [item for item in menu_items if item['category'] == category]
                for item in category_items:
                    with cat_col1: st.text(item['item_name'])
                    with cat_col2: st.text(f"₹{item['price']:.2f}")
                    with cat_col3: st.button("Add", key=f"add_{item['item_id']}", on_click=add_item_to_order, args=(item,))

    # --- BILLING COLUMN (Right Side) ---
    with bill_col:
        st.header("🛒 Current Order")
        if not st.session_state.current_order:
            st.info("Your order is empty. Add items from the menu.")
        else:
            # Display current order items
            for i, item in enumerate(st.session_state.current_order):
                item_col1, item_col2, item_col3, item_col4 = st.columns([2, 1, 1, 1])
                with item_col1: st.text(item['item_name'])
                with item_col2: st.text(f"x {item['quantity']}")
                with item_col3: st.text(f"₹{item['price'] * item['quantity']:.2f}")
                with item_col4: st.button("Remove", key=f"remove_{item['item_id']}", on_click=remove_item_from_order, args=(item['item_id'],))
            
            st.markdown("---")

            # --- BILL CALCULATION ---
            bill_details = calculator.calculate_bill(st.session_state.current_order)
            st.subheader(f"Subtotal: ₹{bill_details['subtotal']:.2f}")
            st.subheader(f"GST: ₹{bill_details['total_gst']:.2f}")
            
            # --- DISCOUNT AND PAYMENT ---
            discount = st.number_input("Discount (%)", min_value=0.0, max_value=100.0, value=0.0, step=5.0)
            final_bill = calculator.calculate_bill(st.session_state.current_order, discount)
            
            st.markdown("### **Grand Total: ₹" + f"{final_bill['grand_total']:.2f}**")
            
            order_type = st.selectbox("Order Type", ["Dine-In", "Takeaway"])
            payment_method = st.selectbox("Payment Method", ["Cash", "Card", "UPI"])

            # --- GENERATE BILL BUTTON ---
            if st.button("Generate & Save Bill", type="primary"):
                order_details_to_save = {
                    "order_type": order_type,
                    "payment_method": payment_method,
                    "subtotal": final_bill['subtotal'],
                    "total_gst": final_bill['total_gst'],
                    "discount_percentage": discount,
                    "grand_total": final_bill['grand_total']
                }

                order_id = db_utils.save_order(order_details_to_save, st.session_state.current_order)

                if order_id:
                    # --- CHANGE #2: Set the success flag instead of showing the message directly ---
                    st.session_state.show_success = True
                    st.session_state.success_message = f"Bill Generated! Order ID: {order_id}"
                    st.session_state.current_order = []
                    st.rerun() 
                else:
                    st.error("Failed to save the order. Please check logs.")
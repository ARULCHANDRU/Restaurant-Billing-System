# test_calculator.py
from utils import calculator

print("--- Starting Calculator Test ---")

# Simulate a customer's order:
# - 1 Pepperoni Pizza (450, 5% GST)
# - 2 Cokes (60 each, 12% GST)
test_order = [
    {"item_name": "Pepperoni Pizza", "price": 450.0, "quantity": 1, "gst_percentage": 5.0},
    {"item_name": "Coca-Cola", "price": 60.0, "quantity": 2, "gst_percentage": 12.0}
]

# Set a discount for the order
test_discount = 10.0 # 10% discount

# Call the function from our calculator module
bill_details = calculator.calculate_bill(test_order, test_discount)

# --- Print a nicely formatted bill ---
print("\n--- Test Bill ---")
print(f"Order Items: {len(test_order)}")
print(f"Discount Applied: {test_discount}%")
print("-------------------")
print(f"Subtotal:          ₹{bill_details['subtotal']:.2f}")
print(f"Total GST:         + ₹{bill_details['total_gst']:.2f}")
print(f"Discount Amount:   - ₹{bill_details['discount_amount']:.2f}")
print("===================")
print(f"GRAND TOTAL:       ₹{bill_details['grand_total']:.2f}")
print("\n--- Calculator Test Complete ---")
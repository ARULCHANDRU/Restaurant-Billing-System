# utils/calculator.py

def calculate_bill(items, discount_percentage=0):
    """
    Calculates the bill breakdown from a list of items and an optional discount.

    Args:
        items (list): A list of dictionaries, where each dictionary represents an item.
                      Expected keys: 'price', 'quantity', 'gst_percentage'.
        discount_percentage (float): The discount to apply to the subtotal, in percent.

    Returns:
        dict: A dictionary containing the bill breakdown (subtotal, total_gst,
              discount_amount, grand_total).
    """
    subtotal = 0
    total_gst = 0

    # Calculate subtotal and total GST by iterating through each item
    for item in items:
        item_total = item['price'] * item['quantity']
        gst_on_item = item_total * (item['gst_percentage'] / 100)
        
        subtotal += item_total
        total_gst += gst_on_item

    # Calculate discount amount from the subtotal
    discount_amount = subtotal * (discount_percentage / 100)

    # Calculate the final grand total
    grand_total = (subtotal - discount_amount) + total_gst

    # Return all calculated values in a structured dictionary
    return {
        "subtotal": round(subtotal, 2),
        "total_gst": round(total_gst, 2),
        "discount_amount": round(discount_amount, 2),
        "grand_total": round(grand_total, 2)
    }
# Restaurant Billing Software

This project is a complete, web-based billing application for restaurants built with Python and Streamlit. It handles order entry, dynamic bill calculation with GST and discounts, secure data storage, and provides an analytics dashboard for sales reporting.

## Key Features

- **Interactive UI:** A clean and modern web interface built with Streamlit.
- **Dynamic Menu:** The menu is loaded directly from the database and displayed by category.
- **Real-time Bill Calculation:** The order summary and grand total update instantly as items are added or discounts are applied.
- **Persistent Storage:** All completed transactions are saved to a robust SQLite database.
- **Multi-Page Navigation:** A sidebar allows easy switching between the `Billing` interface and the `Reports` dashboard.
- **Sales Analytics:** The reports page displays key metrics, a breakdown of most-sold items, and daily sales charts.

## Technology Stack

- **Backend:** Python
- **UI:** Streamlit
- **Database:** SQLite3
- **Data Analysis:** pandas

## Project Structure

restaurant_billing/
├── app.py              # Main application entry point
├── db/
│   └── restaurant.db
├── data/
│   └── menu.csv
├── ui/
│   ├── main_ui.py
│   └── reports_ui.py
├── utils/
│   ├── calculator.py
│   └── db_utils.py
├── README.md
└── requirements.txt


## How to Set Up and Run

1.  **Clone the repository:**
    ```sh
    git clone <your-repo-link>
    cd restaurant_billing
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    # Create
    python -m venv venv
    # Activate (Windows)
    venv\Scripts\activate
    # Activate (macOS/Linux)
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```sh
    streamlit run app.py
    ```

The application will be available in your web browser at `http://localhost:8501`.

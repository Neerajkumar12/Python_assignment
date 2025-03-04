# Python ETL Pipeline and JokeAPI Integration

## Overview
This project consists of two parts:
1. **ETL Pipeline**: Processes sales data from two regions, applies business rules, and stores the transformed data in an SQLite database.
2. **Flask API**: Fetches jokes from JokeAPI, processes them, and stores them in an SQLite database.

---

## File Structure
project/
│
├── etl_pipeline/
│ ├── etl_script.py # Python script for ETL process (Question 1)
│ ├── sales_data.db # SQLite database for transformed sales data
│ ├── data/
│ │ ├── order_region_a.csv # Sales data file for Region A
│ │ ├── order_region_b.csv # Sales data file for Region B
│
├── joke_api/
│ ├── joke_api.py # Flask API script (Question 2)
│ ├── jokes.db # SQLite database to store jokes
│
├── README.md # Instructions for running the program
└── requirements.txt # Python dependencies for the project



---

## Prerequisites
- Python 3.x installed.
- Install required libraries using:


pip install -r requirements.txt


---

## Part 1: ETL Pipeline (Sales Data)

### Steps to Run:
1. Navigate to the `etl_pipeline/` directory:
  ```
  cd etl_pipeline/
  ```
2. Place your CSV files (`order_region_a.csv`, `order_region_b.csv`) inside the `data/` folder.
3. Run the ETL script:
  ```
  python etl_script.py
  ```
4. The transformed data will be stored in an SQLite database named `sales_data.db`.

### Validation Queries:
- The script includes SQL queries to validate:
- Total records in the database.
- Total sales by region.
- Average sales per transaction.
- Duplicate `OrderId` checks.

---

## Part 2: Flask API (JokeAPI Integration)

### Steps to Run:
1. Navigate to the `joke_api/` directory:
  ```
  cd joke_api/
  ```
2. Run the Flask app:
  ```
  python joke_api.py
  ```
3. Access the following endpoints:
  - **Fetch Jokes**: [http://127.0.0.1:5000/fetch-jokes](http://127.0.0.1:5000/fetch-jokes)  
    Fetches jokes from JokeAPI and stores them in `jokes.db`.
  - **Get Jokes**: [http://127.0.0.1:5000/get-jokes](http://127.0.0.1:5000/get-jokes)  
    Retrieves all jokes stored in the database.

---

## Assumptions & Decisions

- SQLite is used as a lightweight database solution.
- Duplicate `OrderId`s are removed during transformation in Part 1.
- Only valid jokes are stored in Part 2.

---

## Notes

- Ensure CSV files have correct column names as per schema.
- Modify configurations (e.g., database name) if needed.

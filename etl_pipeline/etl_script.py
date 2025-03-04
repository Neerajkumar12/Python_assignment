import pandas as pd
import sqlite3

# Step 1: Extract Data
def extract_data(file_path, region):
    """Read CSV data and add a region column."""
    data = pd.read_csv(file_path)
    data.columns = [col.strip() for col in data.columns]  # Remove leading spaces
    print(f"Column names for {file_path}: {data.columns}")
    data['region'] = region
    return data

# Step 2: Transform Data
def transform_data(data):
    """Apply business rules to clean and transform the data."""
    required_columns = ['OrderId', 'OrderItemId', 'QuantityOrdered', 'ItemPrice', 'PromotionDiscount']
    
    # Check if all required columns exist
    if not all(col in data.columns for col in required_columns):
        missing_columns = [col for col in required_columns if col not in data.columns]
        print(f"Error: Missing columns - {missing_columns}")
        return None  # or handle it as per your requirement
    
    # Calculate total_sales
    data['total_sales'] = data['QuantityOrdered'] * data['ItemPrice']
    
    # Calculate net_sale
    data['net_sale'] = data['total_sales'] - data['PromotionDiscount']
    
    # Remove duplicates based on OrderId
    data = data.drop_duplicates(subset='OrderId')
    
    # Filter out rows where net_sale <= 0
    data = data[data['net_sale'] > 0]
    
    return data

# Step 3: Load Data
def load_data(data, db_name='sales_data.db'):
    """Load transformed data into SQLite database."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_data (
            OrderId INTEGER PRIMARY KEY,
            OrderItemId INTEGER,
            QuantityOrdered INTEGER,
            ItemPrice REAL,
            PromotionDiscount REAL,
            region TEXT,
            total_sales REAL,
            net_sale REAL
        )
    ''')
    
    # Insert data into the table
    data.to_sql('sales_data', conn, if_exists='replace', index=False)
    
    conn.commit()
    conn.close()

# SQL Validation Queries
def validate_data(db_name='sales_data.db'):
    """Run SQL queries to validate the loaded data."""
    conn = sqlite3.connect(db_name)
    
    print("Total Records:", pd.read_sql_query("SELECT COUNT(*) FROM sales_data", conn).iloc[0, 0])
    
    print("Total Sales by Region:")
    print(pd.read_sql_query("SELECT region, SUM(total_sales) AS total_sales FROM sales_data GROUP BY region", conn))
    
    print("Average Sales per Transaction:")
    print(pd.read_sql_query("SELECT AVG(net_sale) AS avg_sales FROM sales_data", conn).iloc[0, 0])
    
    print("Duplicate OrderId Check:")
    print(pd.read_sql_query("SELECT OrderId, COUNT(*) FROM sales_data GROUP BY OrderId HAVING COUNT(*) > 1", conn))
    
    conn.close()

if __name__ == "__main__":
    # File paths and regions
    file_a = "data/order_region_a.csv"
    file_b = "data/order_region_b.csv"
    
    # Extract Data
    region_a_data = extract_data(file_a, 'A')
    region_b_data = extract_data(file_b, 'B')
    
    # Combine Data from Both Regions
    combined_data = pd.concat([region_a_data, region_b_data])
    
    # Transform Data
    transformed_data = transform_data(combined_data)
    
    if transformed_data is not None:
        # Load Data into SQLite Database
        load_data(transformed_data)
        
        # Validate Data with SQL Queries
        validate_data()
    else:
        print("Transformation failed due to missing columns.")

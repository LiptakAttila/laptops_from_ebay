import os
import pyodbc
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

db_password = os.getenv("Password")
db_username = os.getenv("Username")

conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost;"
    "Database=WideWorldImporters;"
    "Trusted_connection=yes;"
    f"UID={db_username};"
    f"PWD={db_password};"
)
# create
cursor = conn.cursor()

df = pd.read_csv(r"C:\Users\Dell\OneDrive\Bureaublad\projects\laptops_ebay\laptops_from_ebay\ebay_laptops.csv")

laptop_brands = [
    'Dell',
    'HP',
    'Lenovo',
    'Asus',
    'Acer',
    'Apple',
    'Microsoft',
    'MSI',
    'Samsung',
    'Toshiba',
    'Sony',
    'Fujitsu',
    'LG',
    'Huawei',
    'Razer',
    'Major Brand',
    'Top Brand'
]

def create_table_func():
    drop_table = "IF OBJECT_ID('Laptop', 'U') IS NOT NULL DROP TABLE Laptop;"
    create_statement = """CREATE TABLE Laptop (
                        name VARCHAR(255),
                        state VARCHAR(255),
                        price FLOAT,
                        brand VARCHAR(255)                      
                        )
    """
    cursor.execute(drop_table)
    cursor.execute(create_statement)
    cursor.commit()

def transform_data():

    # Price

    clean_prices = df['Laptop price'].str.replace('$', '').str.replace('£', '').str.replace(',', '').str.split(' to ', expand=True).astype(float)
    df['Price'] = clean_prices.mean(axis=1)

    # Brand

    brand_pattern = '|'.join(laptop_brands)
    brands = df['Lap Details'].str.extract('({})'.format(brand_pattern))

    # Extract the first non-null value from each row
    df['Brand'] = brands.ffill(axis=1).iloc[:, -1]
    df['Brand'] = df['Brand'].fillna('unknown brand')

    # Remove duplicates and drop NaN values
    unique_brands = df['Brand'].dropna().drop_duplicates()

    return df


def insert_func():
    data = transform_data()
    print(data)

create_table_func()
insert_func()
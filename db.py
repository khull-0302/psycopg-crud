import psycopg2
import os


database_name = os.environ.get('DATABASE_NAME')


conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()

def create_all():
    print('creating tables...')

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS Companies (
                   company_id UUID PRIMARY KEY,
                   company_name VARCHAR UNIQUE NOT NULL);
                   
                   CREATE TABLE IF NOT EXISTS Categories (
                   category_id UUID PRIMARY KEY,
                   category_name VARCHAR UNIQUE NOT NULL);
                   
                   CREATE TABLE IF NOT EXISTS Products (
                   product_id UUID PRIMARY KEY,
                   company_id UUID NOT NULL,
                   product_name VARCHAR UNIQUE NOT NULL,
                   price FLOAT,
                   description VARCHAR,
                   active BOOLEAN DEFAULT True,
                   FOREIGN KEY (company_id) REFERENCES Companies(company_id));
                   
                   CREATE TABLE IF NOT EXISTS Warranties (
                   warranty_id UUID PRIMARY KEY,
                   product_id UUID NOT NULL,
                   warranty_months INTEGER NOT NULL,
                   FOREIGN KEY (product_id) REFERENCES Products(product_id));
                   
                   CREATE TABLE IF NOT EXISTS ProductsCategoriesXref (
                   product_id UUID NOT NULL,
                   category_id UUID NOT NULL,
                   PRIMARY KEY (product_id, category_id),
                   FOREIGN KEY (product_id) REFERENCES Products(product_id),
                   FOREIGN KEY (category_id) REFERENCES Categories(category_id)
                   );
                   """)
    conn.commit()
    print('Tables are now created')
from flask import jsonify, request
import psycopg2
import os

database_name = os.environ.get('DATABASE_NAME')

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()

def create_product():
    post_data = request.form if request.form else request.json

    product_name = post_data.get('product_name')
    description = post_data.get('description')
    price = post_data.get('price')
    active = post_data.get('active', True)

    if not product_name:
        return jsonify({'message': 'product name required'}),400
    
    cursor.execute("""SELECT * FROM  Products WHERE product_name = %s""", (product_name))

    existing_product = cursor.fetchone()

    if existing_product:
        return jsonify({"message": "product already exists"}),400
    
    try:
        cursor.execute("""
                   INSERT INTO Products (
                   product_name,
                   description,
                   price,
                   active
                ) VALUES (
                   %s,
                   %s,
                   %s,
                   %s
                   )
                """, (product_name, description, price, active))
        conn.commit()
    
    except:
        cursor.rollback()
        return jsonify({'message': 'product could not be added'}),400


    return jsonify({"message": f"product {product_name} has been added to the database"}),201


def get_all_products():
    cursor.execute("""SELECT * FROM Products;""")
    results = cursor.fetchall()

    product_list = []

    for record in results:
        product_record = {
            'product_id': record[0],
            'company_id': record[1],
            'product_name': record[2],
            'price': record[3],
            'description': record[4],
            'active': record[5]
        }

        product_list.append(product_record)

    return jsonify({"message": "products found", "results": product_list})

def update_product(product_id):
    post_data = request.form if request.form else request.json

    product_name = post_data.get('product_name')
    company_id = post_data.get('company_id')
    description = post_data.get('description')
    price = post_data.get('price')
    active = post_data.get('active')

    cursor.execute(
        "SELECT * FROM Products WHERE product_id = %s",
        (product_id,)
    )

    existing_product = cursor.fetchone()

    if not existing_product:
        return jsonify({"message": "product not found"}), 404

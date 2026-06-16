from flask import jsonify, request
import psycopg2
import os

database_name = os.environ.get('DATABASE_NAME')

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()

def create_product():
    post_data = request.form if request.form else request.json
    
    company_id = post_data.get('company_id')
    product_name = post_data.get('product_name')
    description = post_data.get('description')
    price = post_data.get('price')
    active = post_data.get('active', True)

    if not product_name:
        return jsonify({'message': 'product name required'}),400
    
    cursor.execute("""SELECT * FROM  Products WHERE product_name = %s""", (product_name,))

    existing_product = cursor.fetchone()

    if existing_product:
        return jsonify({"message": "product already exists"}),400
    
    try:
        cursor.execute("""
                   INSERT INTO Products (
                   company_id,
                   product_name,
                   description,
                   price,
                   active
                ) VALUES (
                   %s,
                   %s,
                   %s,
                   %s,
                   %s
                   )
                """, (company_id, product_name, description, price, active))
        conn.commit()
    
    except:
        conn.rollback()
        return jsonify({'message': 'product could not be added'}),400


    return jsonify({"message": f"product {product_name} has been added to the database"}),201


def get_all_products():
    cursor.execute("SELECT * FROM Products;")
    results = cursor.fetchall()

    products_list = []

    for record in results:
        product_id = record[0]

        cursor.execute("""
            SELECT * FROM Warranties
            WHERE product_id = %s
        """, (product_id,))

        warranty = cursor.fetchone()

        warranty_record = None

        if warranty is not None:
            warranty_record = {
                'warranty_id': warranty[0],
                'product_id': warranty[1],
                'warranty_months': warranty[2]
            }

        cursor.execute("""
            SELECT c.category_id, c.category_name
            FROM Categories c
            JOIN ProductsCategoriesXref xref
                ON c.category_id = xref.category_id
            WHERE xref.product_id = %s
        """, (product_id,))

        categories = cursor.fetchall()

        category_list = [
            {
                'category_id': category[0],
                'category_name': category[1]
            }
            for category in categories
        ]

        product_record = {
            'product_id': record[0],
            'company_id': record[1],
            'product_name': record[2],
            'price': record[3],
            'description': record[4],
            'active': record[5],
            'warranty': warranty_record,
            'categories': category_list
        }

        products_list.append(product_record)

    return jsonify({
        "message": "products found",
        "results": products_list
    }), 200

def get_active_products():
    cursor.execute("""SELECT * FROM Products WHERE active = True;""")
    results = cursor.fetchall()

    active_products_list = []

    for record in results:
        active_product_record = {
            'product_id': record[0],
            'company_id': record[1],
            'product_name': record[2],
            'price': record[3],
            'description': record[4],
            'active': record[5]
        }

        active_products_list.append(active_product_record)

    return jsonify({"message": "active products found", "results": active_products_list}),200

def get_product_by_id(product_id):

    cursor.execute("""
        SELECT * FROM Products WHERE product_id = %s""", (product_id,))

    product = cursor.fetchone()

    if not product:
        return jsonify({"message": "product not found"}), 404

    cursor.execute("""
        SELECT c.category_id, c.category_name
        FROM Categories c
        JOIN ProductsCategoriesXref xref
            ON c.category_id = xref.category_id
        WHERE xref.product_id = %s
    """, (product_id,))

    categories = cursor.fetchall()

    category_list = []

    for category in categories:
        category_list.append({
            'category_id': category[0],
            'category_name': category[1]
        })

    product_record = {
        'product_id': product[0],
        'company_id': product[1],
        'product_name': product[2],
        'price': product[3],
        'description': product[4],
        'active': product[5],
        'categories': category_list
    }

    return jsonify({"message": "product found", "result": product_record}), 200

def get_product_by_company_id(company_id):

    cursor.execute("""SELECT * FROM Products WHERE company_id = %s""", (company_id,))
    
    products = cursor.fetchall()

    if not products:
        return jsonify({"message": "products not found"}), 404
    
    products_list = []

    for product in products:

        product_record = {
            'product_id': product[0],
            'company_id': product[1],
            'product_name': product[2],
            'price': product[3],
            'description': product[4],
            'active': product[5]
        }

        products_list.append(product_record)

    return jsonify({
        "message": "products found",
        "results": products_list
    }), 200


def create_product_category():
    post_data = request.form if request.form else request.json

    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')

    if not product_id:
        return jsonify({'message': 'product_id required'}), 400

    if not category_id:
        return jsonify({'message': 'category_id required'}), 400

    cursor.execute("""
        SELECT * FROM ProductsCategoriesXref
        WHERE product_id = %s
        AND category_id = %s
    """, (product_id, category_id))

    existing_association = cursor.fetchone()

    if existing_association:
        return jsonify({'message': 'association already exists'}), 400

    try:
        cursor.execute("""
            INSERT INTO ProductsCategoriesXref (
                product_id,
                category_id
            ) VALUES (
                %s,
                %s
            )
        """, (product_id, category_id,))

        conn.commit()

    except:
        conn.rollback()
        return jsonify({'message': 'association could not be added'}), 400

    return jsonify({
        'message': f'product {product_id} linked to category {category_id}'
    }), 201




def update_product(product_id):
    post_data = request.form if request.form else request.json
    product_id = int(product_id)

    cursor.execute(
        "SELECT * FROM Products WHERE product_id = %s",
        (product_id,)
    )

    existing_product = cursor.fetchone()

    if not existing_product:
        return jsonify({"message": "product not found"}), 404
    
    product_name = post_data.get('product_name')
    description = post_data.get('description')
    price = post_data.get('price')
    active = post_data.get('active')


    cursor.execute("""UPDATE Products SET 
                   product_name = %s, 
                   description = %s, 
                   price = %s,
                   active = %s
                   WHERE product_id = %s""",
                   (product_name, description, price, active, product_id))
    conn.commit()

    cursor.execute(
        "SELECT * FROM Products WHERE product_id = %s",
        (product_id,)
    )

    result = cursor.fetchone()

    product_record = {
            'product_id': result[0],
            'company_id': result[1],
            'product_name': result[2],
            'price': result[3],
            'description': result[4],
            'active': result[5]
        }    

    return jsonify({"message": "product updated", "result": product_record}), 200

def delete_product(product_id):
    product_id = int(product_id)

    cursor.execute(
        "SELECT * FROM Products WHERE product_id = %s",
        (product_id,)
    )

    existing_product = cursor.fetchone()

    if not existing_product:
        return jsonify({"message": "product not found"}), 404

    try:
        cursor.execute(
            "DELETE FROM ProductsCategoriesXref WHERE product_id = %s",
            (product_id,)
        )

        cursor.execute(
            "DELETE FROM Warranties WHERE product_id = %s",
            (product_id,)
        )

        cursor.execute(
            "DELETE FROM Products WHERE product_id = %s",
            (product_id,)
        )
        conn.commit()

    except:
        conn.rollback()
        return jsonify({"message": "product could not be deleted"}), 400

    return jsonify({"message": f"product {product_id} deleted successfully"}), 200



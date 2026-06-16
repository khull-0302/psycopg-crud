from flask import jsonify, request
import psycopg2
import os

database_name = os.environ.get('DATABASE_NAME')

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()

def create_category():
    post_data = request.form if request.form else request.json

    category_name = post_data.get('category_name')

    if not category_name:
        return jsonify({'message': 'category name required'}), 400

    cursor.execute("""
        SELECT * FROM Categories
        WHERE category_name = %s
    """, (category_name,))

    existing_category = cursor.fetchone()

    if existing_category:
        return jsonify({"message": "category already exists"}), 400

    try:
        cursor.execute("""
            INSERT INTO Categories (
                category_name
            ) VALUES (
                %s
            )
        """, (category_name,))

        conn.commit()

    except:
        conn.rollback()
        return jsonify({'message': 'category could not be added'}), 400

    return jsonify({
        "message": f"category {category_name} has been added to the database"
    }), 201

def get_categories():
    cursor.execute("""SELECT * FROM Categories;""")
    results = cursor.fetchall()

    categories_list = []

    for record in results:
        category_record = {
            'category_id': record[0],
            'category_name': record[1]
        }

        categories_list.append(category_record)

    return jsonify({"message": "categories found", "results": categories_list}),200

def get_category_by_id(category_id):

    cursor.execute("""SELECT * FROM Categories WHERE category_id = %s""", (category_id,))

    category = cursor.fetchone()

    if not category:
        return jsonify({"message": "category not found"}), 404

    category_record = {
        "category_id": category[0],
        "category_name": category[1]
    }

    return jsonify({"message": "category found", "result": category_record}),200

def update_category_by_id(category_id):
    post_data = request.form if request.form else request.json
    category_id = int(category_id)

    cursor.execute(
        "SELECT * FROM Categories WHERE category_id = %s",
        (category_id,)
    )

    existing_category = cursor.fetchone()

    if not existing_category:
        return jsonify({"message": "category not found"}), 404
    
    category_name = post_data.get('category_name')

    cursor.execute("""UPDATE Categories SET 
                   category_name = %s
                   WHERE category_id = %s""",
                   (category_name, category_id))
    conn.commit()

    cursor.execute(
        "SELECT * FROM Categories WHERE category_id = %s",
        (category_id,)
    )

    result = cursor.fetchone()

    category_record = {
            'category_id': result[0],
            'category_name': result[1]
        }    

    return jsonify({"message": "category updated", "result": category_record}), 200

def delete_category(category_id):
    category_id = int(category_id)

    cursor.execute(
        "SELECT * FROM Categories WHERE category_id = %s",
        (category_id,)
    )

    existing_category = cursor.fetchone()

    if not existing_category:
        return jsonify({"message": "category not found"}), 404

    try:
        # delete xref records first
        cursor.execute(
            "DELETE FROM ProductsCategoriesXref WHERE category_id = %s",
            (category_id,)
        )

        # delete category
        cursor.execute(
            "DELETE FROM Categories WHERE category_id = %s",
            (category_id,)
        )

        conn.commit()

    except:
        conn.rollback()
        return jsonify({"message": "category could not be deleted"
        }), 400

    return jsonify({
        "message": f"category {category_id} deleted successfully"
    }), 200

from flask import jsonify, request
import psycopg2
import os

database_name = os.environ.get('DATABASE_NAME')

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()

def create_warranty():
    post_data = request.form if request.form else request.json

    product_id = post_data.get('product_id')
    warranty_months = post_data.get('warranty_months')

    if not product_id:
        return jsonify({'message': 'product_id required'}), 400

    if not warranty_months:
        return jsonify({'message': 'warranty_months required'}), 400

    cursor.execute("""
        SELECT * FROM Warranties
        WHERE product_id = %s
    """, (product_id,))

    existing = cursor.fetchone()

    if existing:
        return jsonify({
            "message": "warranty already exists for this product"
        }), 400

    try:
        cursor.execute("""
            INSERT INTO Warranties (
                product_id,
                warranty_months
            ) VALUES (
                %s,
                %s
            )
        """, (product_id, warranty_months))

        conn.commit()

        return jsonify({
            "message": f"warranty for product_id {product_id} has been created"
        }), 201

    except:
        conn.rollback()
        return jsonify({'message': 'warranty could not be added'}), 400
    
def get_warranty(warranty_id):
    cursor.execute(
        """SELECT * FROM Warranties WHERE warranty_id = %s;""",
        (warranty_id,)
    )

    record = cursor.fetchone()

    if record is None:
        return jsonify({"message": "warranty not found"}), 404

    warranty_record = {
        'warranty_id': record[0],
        'product_id': record[1],
        'warranty_months': record[2]
    }

    return jsonify({
        "message": "warranty found",
        "result": warranty_record
    }), 200

def update_warranty_by_id(warranty_id):
    post_data = request.get_json(silent=True) or request.form
    warranty_id = int(warranty_id)

    cursor.execute(
        "SELECT * FROM Warranties WHERE warranty_id = %s",
        (warranty_id,)
    )

    existing_warranty = cursor.fetchone()

    if not existing_warranty:
        return jsonify({"message": "warranty not found"}), 404

    product_id = post_data.get('product_id', existing_warranty[1])
    warranty_months = post_data.get('warranty_months', existing_warranty[2])

    cursor.execute(
        """
        UPDATE Warranties
        SET product_id = %s,
            warranty_months = %s
        WHERE warranty_id = %s
        """,
        (product_id, warranty_months, warranty_id)
    )

    conn.commit()

    cursor.execute(
        "SELECT * FROM Warranties WHERE warranty_id = %s",
        (warranty_id,)
    )

    result = cursor.fetchone()

    warranty_record = {
        "warranty_id": result[0],
        "product_id": result[1],
        "warranty_months": result[2]
    }

    return jsonify({
        "message": "warranty updated",
        "result": warranty_record
    }), 200

def delete_warranty(warranty_id):
    warranty_id = int(warranty_id)

    cursor.execute(
        "SELECT * FROM Warranties WHERE warranty_id = %s",
        (warranty_id,)
    )

    existing_warranty = cursor.fetchone()

    if not existing_warranty:
        return jsonify({"message": "warranty not found"}), 404

    try:
        cursor.execute(
            "DELETE FROM Warranties WHERE warranty_id = %s",
            (warranty_id,)
        )

        conn.commit()

    except:
        conn.rollback()
        return jsonify({
            "message": "warranty could not be deleted"
        }), 400

    return jsonify({
        "message": f"warranty {warranty_id} deleted successfully"
    }), 200
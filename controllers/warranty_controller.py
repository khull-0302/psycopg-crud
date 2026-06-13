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

    try:
        cursor.execute("""
            INSERT INTO Warranties (
                       product_id,
                       warranty_months
                       ) VALUES (
                       %s,
                       %s
                       )
                       """, (product_id, warranty_months,))

        conn.commit()

        return jsonify({"message": f"warranty for product_id {product_id} has been created"}),201

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
        "results": warranty_record
    }), 200
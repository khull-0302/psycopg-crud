from flask import jsonify, request
import psycopg2
import os

database_name = os.environ.get('DATABASE_NAME')

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()

def create_company():
    post_data = request.form if request.form else request.json

    company_name = post_data.get('company_name')

    if not company_name:
        return jsonify({'message': 'Company name required'}),400
    
    cursor.execute("""SELECT * FROM  Companies WHERE company_name = %s""", (company_name,))

    existing_company = cursor.fetchone()

    if existing_company:
        return jsonify({"message": "Company already exists"}),400
    
    
    cursor.execute("""INSERT INTO Companies (company_name) VALUES (%s)""", (company_name,))
    conn.commit()

    
    return jsonify({"message": f"Company {company_name} has been added to the database"}),201

def get_all_companies():
    cursor.execute("""SELECT * FROM Companies;""")
    results = cursor.fetchall()

    companies_list = []

    for record in results:
        company_record = {
            'company_id': record[0],
            'company_name': record[1]
        }

        companies_list.append(company_record)

    return jsonify({"message": "companies found", "results": companies_list}),200


def get_company(company_id):
    cursor.execute("""SELECT * FROM Companies WHERE company_id = %s;""", (company_id,))
    result = cursor.fetchone()

    if not result:
        return jsonify({"message": "company not found"}), 404

    company_record = {
        'company_id': result[0],
        'company_name': result[1]
        }

    return jsonify({"message": "company found", "result": company_record}),200

def update_company_by_id(company_id):
    post_data = request.form if request.form else request.json
    company_id = int(company_id)

    cursor.execute(
        "SELECT * FROM Companies WHERE company_id = %s",
        (company_id,)
    )

    existing_company = cursor.fetchone()

    if not existing_company:
        return jsonify({"message": "company not found"}), 404
    
    company_name = post_data.get('company_name')

    cursor.execute("""UPDATE Companies SET 
                   company_name = %s
                   WHERE company_id = %s""",
                   (company_name, company_id))
    conn.commit()

    cursor.execute(
        "SELECT * FROM Companies WHERE company_id = %s",
        (company_id,)
    )

    result = cursor.fetchone()

    company_record = {
            'company_id': result[0],
            'company_name': result[1]
        }    

    return jsonify({"message": "company updated", "result": company_record}), 200




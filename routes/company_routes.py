from flask import Blueprint
import controllers

company = Blueprint('company', __name__)

@company.route('/company', methods=['POST'])
def create_company_route():
    return controllers.create_company()

@company.route('/companies', methods=['GET'])
def get_companies_route():
    return controllers.get_all_companies()

@company.route('/company/<company_id>', methods=['GET'])
def get_company_route(company_id):
    return controllers.get_company(company_id)


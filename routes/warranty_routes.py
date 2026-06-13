from flask import Blueprint
import controllers

warranty = Blueprint('warranty', __name__)

@warranty.route('/warranty', methods=['POST'])
def create_warranty_route():
    return controllers.create_warranty()

@warranty.route('/warranty/<warranty_id>', methods=['GET'])
def get_warranty_route(warranty_id):
    return controllers.get_warranty(warranty_id)
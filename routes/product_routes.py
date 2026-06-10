from flask import Blueprint
import controllers

product = Blueprint('product', __name__)

@product.route('/product', methods=['POST'])
def create_product_route():
    return controllers.create_product()

@product.route('/products', methods=['GET'])
def get_products_route():
    return controllers.get_all_products()

@product.route('/product', methods=['PATCH'])
def update_product_route():
    return controllers.update_product()
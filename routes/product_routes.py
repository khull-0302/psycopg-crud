from flask import Blueprint
import controllers

product = Blueprint('product', __name__)

@product.route('/product', methods=['POST'])
def create_product_route():
    return controllers.create_product()

@product.route('/products', methods=['GET'])
def get_products_route():
    return controllers.get_all_products()

@product.route('/products/active', methods= ['GET'])
def get_active_products_route():
    return controllers.get_active_products()

@product.route('/product/<product_id>', methods=['GET'])
def get_product_by_id_route(product_id):
    return controllers.get_product_by_id(product_id)

@product.route('/product/category', methods=['POST'])
def create_product_category_route():
    return controllers.create_product_category()

@product.route('/product/<product_id>', methods=['PUT'])
def update_product_route(product_id):
    return controllers.update_product(product_id)

@product.route('/product/delete/<product_id>', methods=['DELETE'])
def delete_product_route(product_id):
    return controllers.delete_product(product_id)
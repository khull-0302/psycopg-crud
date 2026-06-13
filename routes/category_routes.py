from flask import Blueprint
import controllers

category = Blueprint('category', __name__)

@category.route('/category', methods=['POST'])
def create_category_route():
    return controllers.create_category()

@category.route('/categories', methods=['GET'])
def get_categories_route():
    return controllers.get_categories()

@category.route('/category/<category_id>', methods=['GET'])
def get_category_by_id_route(category_id):
    return controllers.get_category_by_id(category_id)


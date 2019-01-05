import os
from flask import request, jsonify, url_for, request, redirect
from flask_restful import Resource, abort, reqparse, marshal
from flask_jwt_extended import jwt_required

from ..helpers.constants import APP_URL
from app import app, mongo
import logger
from app.models import category_model
# ROOT_PATH = os.environ.get('ROOT_PATH')
# LOG = logger.get_root_logger(
#     __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

class Categories(Resource):
    @jwt_required
    def get(self, name=None):
        data = []
        if name:
            cate = category_model.get_category_by_name(name)
            if not cate: 
                return jsonify({ 'ok': False, 'message': 'Category not found' })
            return jsonify({ 'ok': True, 'response': cate }) 
        else:
            results = category_model.get_all_categories()
            for res in results:
                res['url'] = APP_URL + url_for('categories') + '/' + res.get('name')
                data.append(res)
            return jsonify({'response': data})
    
    @jwt_required
    def post(self):
        data = request.json
        if not data:
            return abort(400, message='Data should not be empty')
        else:
            name = data['name']
            if not name:
                return abort(400)
            if category_model.get_category_by_name(name):
                return abort(400, message='Name already exists, try another name')
            if not category_model.add_new_category(data):
                return jsonify({ 'ok': False, 'message': 'Something went wrong' })
        return redirect(url_for('categories'))
    
    @jwt_required
    def delete(self, name):
        mongo.db.categories.remove({ 'name': name })
        return redirect(url_for('categories'))
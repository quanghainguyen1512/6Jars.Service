import os
from flask import request, jsonify, url_for, request, redirect
from flask_restful import Resource, abort, reqparse, marshal
from flask_jwt_extended import jwt_required

from ..helpers.constants import APP_URL
from app import app, mongo
import logger
# ROOT_PATH = os.environ.get('ROOT_PATH')
# LOG = logger.get_root_logger(
#     __name__, filename=os.path.join(ROOT_PATH, 'output.log'))

class Categories(Resource):
    @jwt_required
    def get(self, name=None):
        data = []
        if name:
            results = mongo.db.categories.find({'name': name})
            for res in results:
                res['url'] = APP_URL + url_for('categories') + '/' + res.get('name')
                data.append(res)
            return jsonify({'response': data}) 
        else:
            results = mongo.db.categories.find({}, {'_id': 0})
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
            # name = data.get('name')
            name = data['name']
            if name:
                if mongo.db.categories.find_one({ 'name': name }):
                    return abort(400, message='Name already exists, try another name')
                else:
                    mongo.db.categories.insert(data)
            else:
                return abort(400)
        return redirect(url_for('categories'))
    
    @jwt_required
    def delete(self, name):
        mongo.db.categories.remove({ 'name': name })
        return redirect(url_for('categories'))
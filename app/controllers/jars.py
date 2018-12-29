import os
from flask import request, url_for, jsonify, redirect
from flask_restful import Resource
from ..helpers.constants import APP_URL
from app import app, mongo

class Wallets(Resource):
    def get(self, short_name=None):
        if short_name:
            result = mongo.db.wallets.find_one_or_404({ 'short_name': short_name })
            return jsonify(result)
        else:
            data = []
            results = mongo.db.wallets.find({}, { 'name': 1, 'short_name': 1, 'percentage': 1 })
            for res in results:
                res['url'] = APP_URL + url_for('wallets') + '/' + res['short_name']
                data.append(res)
            return jsonify(data)

    def post(self):
        data = request.get_json()
        if not data: 
            data = { 'response': 'Invalid data' }
            return jsonify(data)
        else:
            pass
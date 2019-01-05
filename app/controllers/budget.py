from flask import request, url_for, jsonify, redirect
from flask_restful import Resource, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.helpers.constants import APP_URL
from app.models import budget_model
from app.schemas import validate_data, budget_schema
from app import mongo

class Budgets(Resource):
    @jwt_required
    def get(self):
        user = get_jwt_identity()
        data = budget_model.get_budget(user)
        return data
    @jwt_required
    def post(self):
        req = request.json
        validation = validate_data(req, budget_schema)
        if not validation['ok']:
            return abort(400, message='Request data is invalid')
        data = validation['data']
        user = get_jwt_identity()
        if not budget_model.update_percent(user, data):
            return abort(500, message='Something went wrong')
        return redirect(url_for('budget'))

import os
from flask import request, url_for, jsonify, redirect
from flask_restful import Resource, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..helpers.constants import APP_URL
from app import app, mongo
from datetime import datetime
from app.models import transaction_model, budget_model
from app.schemas import transaction_schema, validate_data

class Transactions(Resource):
    @jwt_required
    def get(self, tran_id=None):
        user = get_jwt_identity()
        if tran_id:
            res = transaction_model.get_transaction_by_id(user, tran_id)
            if not res:
                return abort(404, message='Transaction not found')
            return jsonify({ 'ok': True, 'response': res })
        else:
            args = request.args
            if not 'start' in args or not 'end' in args:
                return abort(400, message='Request requires timespan arguments')
            start = args['start']
            end = args['end']
            
            try:
                s_date = datetime(start, '%d/%m/%Y')
                e_date = datetime(end, '%d/%m/%Y')
            except ValueError:
                return jsonify({ 'ok': False, 'message': 'Date should have [dd/mm/yyyy] format' })
            result = []
            # user = get_jwt_identity()
            data = transaction_model.get_transactions(s_date, e_date, user)
            for d in data:
                d['url'] = '{}{}/{}'.format(APP_URL, url_for('transactions'), d['_id'])
                result.append(data)
        return jsonify({ 'ok': True, 'response': result})
    @jwt_required
    def post(self):
        # user = get_jwt_identity()
        isValid = validate_data(request.json, transaction_schema)
        if not isValid['ok']:
            return abort(400, message=isValid['message'])
        data = isValid['data']
        res, inserted_id = transaction_model.add_transaction(data)
        if not res:
            return abort(500, message='Something went wrong')
        # if data['type'] == 'expense':
        #     # if not budget_model.check_can_decrease(user, data['jar'], data['value']):
        #     #     return (400, message='')
        #     if not budget_model.update_for_expense(data):
        #         return abort(500, message='Unable to update budget, something went wrong !')
        # elif data['type'] == 'income':
        #     if not budget_model.update_for_income(data):
        #         return abort(500, message='Unable to update budget, something went wrong !')
        if not budget_model.update_budget_for_transaction(data):
            return abort(500, message='Update budget failed, something went wrong')
        return redirect('{}/{}'.format(url_for('transactions'), inserted_id))
        # return jsonify({})
        # return redirect(url_for('transaction'))
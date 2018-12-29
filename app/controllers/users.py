import os
from flask import request, redirect, url_for, jsonify
from flask_restful import Resource, abort, reqparse
import flask_bcrypt
from flask_jwt_extended import ( create_access_token, create_refresh_token, get_jwt_identity,
jwt_refresh_token_required, jwt_required, get_raw_jwt)
from app import mongo
from ..schemas.user import validate_user
from ..models import user_model, revoked_token_model

parser = reqparse.RequestParser()
parser.add_argument('email', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

class UserRegistration(Resource):
    def post(self):
        # data = parser.parse_args()
        res = validate_user(request.json)
        if not res['ok']:
            return jsonify({ 'ok': False, 'message': res['message'] })
        data = res['data']
        if user_model.find_user_by_email(data['email']):
            return jsonify({ 'ok': False, 'message': 'Email already exists' })
        data['password'] = flask_bcrypt.generate_password_hash(data['password'])
        if not user_model.add_new_user(data):
            return abort(500, message='Something went wrong')
        return jsonify({ 'ok': True, 'message': 'Successful registration'})


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = user_model.find_user_by_email(data['email'])
        if not current_user:
            return jsonify({ 'ok': False, 'message': 'User {} doesn\'t exist'.format(data['email']) })

        if flask_bcrypt.check_password_hash(current_user['password'], data['password']):
            del current_user['password']
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            current_user['access_token'] = access_token
            current_user['refresh_token'] = refresh_token
            assert 'password' not in current_user
            return jsonify({
                    'ok': True,
                    'message': 'Logged in as {}'.format(current_user['email']),
                    'data': current_user
                })
        return jsonify({ 'ok': False, 'message': 'Wrong credentials'})
      
      
class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token_model.add(jti)
            return {'message': 'Access token has been revoked'}
        except:
            return abort(500, message='Something went wrong')
      

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token_model.add(jti)
            return {'message': 'Access token has been revoked'}
        except:
            return abort(500, message='Something went wrong')      
    
# class Users(Resource):
#     # def get_all(self):
#     #     return {'message': 'List of users'}
#     @jwt_required
#     def delete(self):
#         data = parser.parse_args()
#         if user_model.delete_user(data['email']):
#             return { 'ok': True, 'message': 'Delete user successfully'}
#         else:
#             return { 'ok': False, 'message': 'Something went wrong'}

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}

class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }
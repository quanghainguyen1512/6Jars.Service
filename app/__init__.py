import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from app import models
import config

class JSONEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    def default(self, o): # pylint: disable=E0202
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__, static_folder='../uploaded_files')
app.config.from_object(config.Config)
app.json_encoder = JSONEncoder

flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mongo = PyMongo(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.revoked_token_model.check_token_is_used(jti)

from app.controllers import *
api = Api(app)
api.add_resource(Categories, '/api/categories', endpoint='categories')
api.add_resource(Categories, '/api/categories/<string:name>', endpoint='name')

api.add_resource(UserRegistration, '/api/registration', endpoint='registration')
api.add_resource(UserLogin, '/api/login', endpoint='login')
api.add_resource(UserLogoutAccess, '/api/logout/access', endpoint='logoutaccess')
api.add_resource(UserLogoutRefresh, '/api/logout/refresh', endpoint='logoutrefresh')
api.add_resource(TokenRefresh, '/api/token/refresh', endpoint='tokenrefresh')
# api.add_resource(Users, '/api/users')
# api.add_resource(Categories, '/api/categories', endpoint='')
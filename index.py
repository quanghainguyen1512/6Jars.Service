import os
import sys
import requests
from flask import jsonify, request, make_response, send_from_directory

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})

# os.environ.update({'PORT': 4000})
# os.environ.update({'ENV': 'development'})

import logger
from app import app

LOG = logger.get_root_logger(os.environ.get(
    'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))

# Port variable to run the server on.
PORT = os.environ.get('PORT')
# PORT = 4000

@app.errorhandler(404)
def not_found(err):
    """ error handler """
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.route('/')
def index():
    """ static files server """
    return send_from_directory('./dist', 'index.html')

# @auth.error_handler
# def unauthorized():
#     # return 403 instead of 401 to prevent browsers from displaying the default
#     # auth dialog
#     return make_response(jsonify({'message': 'Unauthorized access'}), 403)

if __name__ == "__main__":
    LOG.info('running environment: {}'.format(os.environ.get('ENV')))
    LOG.info('Listening to server - port: {}'.format(os.environ.get('PORT')))
    app.config['DEBUG'] = os.environ.get('ENV') == 'development' # Debug mode if development env
    app.run(port=int(PORT), host='0.0.0.0') 
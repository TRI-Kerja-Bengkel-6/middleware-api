from src.portainer import login, createStack
import argparse
import time

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_restx import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app=app,
          version="1.0",
          title="kerbengenam middleware API")

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_SORT_KEYS'] = False

portainer_namespace = api.namespace('portainer', 
                    description='Calling portainer API for multiple purpose')
@ portainer_namespace.route('createStack', methods=['POST'])
class postItems(Resource):
    @ postItems_namespace.doc(
        responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, 
        params={
            'username': {'description': 'Username klien', 'type': 'String', 'required': False},
            'app': {'description': 'Aplikasi yang akan diinstall', 'type': 'String', 'required': False},
    })
    @ cross_origin()
    def post(self):

        # Filter out the request arguments
        parser = reqparse.RequestParser()
        parser.add_argument('username',  required=False, default=None, location='args')
        parser.add_argument('app',  required=False, default=None, location='args')

        args = parser.parse_args()
        task_id = args['username']
        query = args['app']



        return jsonify(data)
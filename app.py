from src.service import service
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

portainer_namespace = api.namespace('v1', 
                    description='Calling portainer API for multiple purpose')
@ portainer_namespace.route('/createStack', methods=['POST'])
class createStack(Resource):
    @ portainer_namespace.doc(
        responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, 
        params={
            'username': {'description': 'Username klien', 'type': 'String', 'required': False},
            'app': {'description': 'Aplikasi yang akan diinstall', 'type': 'String', 'required': False},
            'password': {'description': 'default password yang akan digunakan pada aplikasi tersebut. (phpmyadmin)', 'type': 'String', 'required': False},
            'subdomain': {'description': 'subdomain ingin digunakan', 'type': 'String', 'required': False}
    })
    @ cross_origin()
    def post(self):

        # Filter out the request arguments
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username',  required=False, default=None, location='args')
            parser.add_argument('app',  required=False, default=None, location='args')
            parser.add_argument('password',  required=False, default=None, location='args')
            parser.add_argument('subdomain',  required=False, default=None, location='args')

            args = parser.parse_args()
        except:
            pass

        form = request.form

        username = args['username'] or form['username']
        app = args['app'] or form['app']
        password = args['password'] or form['password'] 
        subdomain = args['subdomain'] or form['subdomain']

        res = service(username, password, app, subdomain)

        return jsonify(res)

if __name__ == '__main__':
    app.secret_key = 'kerbengenam-middleware'
    app.run(debug=True, host="0.0.0.0", port=5000, ssl_context=('./sslcert/cert.pem','./sslcert/key.pem'))

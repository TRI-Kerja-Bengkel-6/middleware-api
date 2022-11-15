from src.service import service
from src.database import MySQL
import argparse
import time
import urllib.request

import firebase_admin
import pyrebase
import json
from functools import wraps
from firebase_admin import credentials, auth
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_restx import Resource, Api, reqparse

app = Flask(__name__)
CORS(app)
api = Api(app=app,
          version="1.0",
          title="kerbengenam middleware API")


app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_SORT_KEYS'] = False

cred = credentials.Certificate('fbAdminConfig.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('fbconfig.json')))

def check_token(f):
    @ cross_origin()
    @ wraps(f)
    def wrap(*args,**kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'},400
        try:
            print(print(request.headers['authorization']))
            user = auth.verify_id_token(request.headers['authorization'].replace('Bearer ',''))
            request.user = user
        except Exception as e:
            print(e)
            return {'message':'Invalid token provided.'},400
        return f(*args, **kwargs)
    return wrap

#Api route to sign up a new user
@app.route('/api/signup')
@cross_origin()
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        return {'message': 'Error missing email or password'},400
    try:
        user = auth.create_user(
               email=email,
               password=password
        )
        return {'message': f'Successfully created user {user.uid}'},200
    except:
        return {'message': 'Error creating user'},400

#Api route to get a new token for a valid user
@app.route('/api/token')
@cross_origin()
def token():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        print(user)
        jwt = user['idToken']
        return {'token': jwt}, 200
    except:
        return {'message': 'There was an error logging in'},400

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
            'subdomain': {'description': 'subdomain ingin digunakan', 'type': 'String', 'required': False},
            'email': {'description': 'user email', 'type': 'String', 'required': False}
    })
    @ cross_origin()
    @ check_token
    def post(self):

        # Filter out the request arguments
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username',  required=False, default=None, location='args')
            parser.add_argument('app',  required=False, default=None, location='args')
            parser.add_argument('password',  required=False, default=None, location='args')
            parser.add_argument('subdomain',  required=False, default=None, location='args')
            parser.add_argument('email',  required=False, default=None, location='args')

            args = parser.parse_args()
        except:
            pass

        form = request.form

        username = args['username'] or form['username']
        app = args['app'] or form['app']
        password = args['password'] or form['password'] 
        subdomain = args['subdomain'] or form['subdomain']
        email = args['email'] or form['email']
        print(form)

        res = service(username, password, app, subdomain)
        try:
           mysql.saving(email, res['app_domain'])
        except:
           pass

        return jsonify(res)

@ portainer_namespace.route('/getUserDomain', methods=['POST'])
class getUserDomain(Resource):
    @ portainer_namespace.doc(
        responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, 
        params={
            'email': {'description': 'user email', 'type': 'String', 'required': False}
    })
    @ check_token
    @ cross_origin()
    def post(self):
        @ cross_origin()
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email',  required=False, default=None, location='args')

            args = parser.parse_args()
        except:
            pass

        form = request.form

        email = args['email'] or form['email']

        res = mysql.load(email)

        return jsonify(res)

@ portainer_namespace.route('/getWebsiteStatus', methods=['POST'])
class getWebsiteStatus(Resource):
    @ portainer_namespace.doc(
        responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'}, 
        params={
            'domain': {'description': 'user email', 'type': 'String', 'required': False}
    })
    @ cross_origin()
    @ check_token
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('domain',  required=False, default=None, location='args')

            args = parser.parse_args()
        except:
            pass

        form = request.form

        domain = args['domain'] or form['domain']

        res = {'status': urllib.request.urlopen(f"https://{domain}").getcode()} 

        return jsonify(res)

if __name__ == '__main__':
    mysql = MySQL()
    app.secret_key = 'kerbengenam-middleware'
    app.run(debug=True, host="0.0.0.0", port=5000)

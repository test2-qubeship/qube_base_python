"""
This is the decorator for login enforcement
"""
from functools import wraps
import json
import os
from flask import request, Response
import requests


auth_url = os.getenv('QUBESHIP_AUTH_URL','https://api.qubeship.io/v1/auth')


def validate_with_qubeship_auth(auth_token):
    """ check if the auth_token is valid
    """
    headers = {'content-type': 'application/json'}
    payload = {'token': auth_token}
    resp = requests.post(auth_url + '/validate',
                         headers=headers, data=json.dumps(payload))
    return resp.status_code


def login_required(f):
    """create parser
    """

    def auth_required():
        """ return error message
        """
        data = {
            'error': 'github authorization required'
        }
        js = json.dumps(data)

        resp = Response(js, status=401, mimetype='application/json')
        return resp

    @wraps(f)
    def decorated_function(*args, **kwargs):
        """ definition of login_required
        """
        bearer_token = request.headers.get('Authorization')
        if not bearer_token:
            return auth_required()

        auth_token = bearer_token.split()[1]
        if not auth_token:
            return auth_required()

        # validate auth_token
        if validate_with_qubeship_auth(auth_token) != 200:
            return auth_required()

        return f(*args, **kwargs)
    return decorated_function
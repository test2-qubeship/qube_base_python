"""
This is the decorator for login enforcement
"""
from functools import wraps
import json
import os
from flask import request, Response
import requests

from qube.src.commons.context import AuthContext

auth_url = os.getenv('QUBESHIP_AUTH_URL', 'https://api.qubeship.io/v1/auth')


def validate_with_qubeship_auth(auth_token):
    """ check if the auth_token is valid
    """
    headers = {'content-type': 'application/json', 'Authorization': auth_token}
    # payload = {'token': auth_token}
    resp = requests.get(auth_url + '/user',
                        headers=headers)
    return resp.text, resp.status_code


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

    def unsupported_token():
        """ return error message
        """
        data = {
            'error': 'master tokens are forbidden instead use org tokens'
        }
        js = json.dumps(data)

        resp = Response(js, status=403, mimetype='application/json')
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
        response, status_code = validate_with_qubeship_auth(auth_token)
        if status_code != 200:
            return auth_required()

        userinfo = json.loads(response)
        if userinfo['type'] != "org":
            return unsupported_token()
        auth_context = AuthContext(userinfo['tenant']['id'],
                                   userinfo['tenant']['orgs'][0]['id'],
                                   userinfo['id'])
        kwargs['authcontext'] = {
            'context': auth_context
        }

        return f(*args, **kwargs)

    return decorated_function

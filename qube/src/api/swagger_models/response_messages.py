from flask_restful_swagger_2 import Schema

"""
the common response messages printed in swagger UI
"""
response_msgs = {
    '200': {
        'description': 'OK'
    },
    '401': {
        'description': 'Unauthorized'
    },
    '400': {
        'description': 'Bad Request'
    },
    '404': {
        'description': 'Not found'
    },
    '500': {
        'description': 'Internal server error'
    }
}


class ErrorModel(Schema):
    type = 'object'
    properties = {
        'message': {
            'type': 'string'
        }
    }
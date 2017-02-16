from flask_restful_swagger_2 import Schema

class HelloModel(Schema):
    type = 'object'
    properties = {
        'id': {
            'type': 'string',
        },
        'name': {
            'type': 'string'
        }
    }
    required = ['name']
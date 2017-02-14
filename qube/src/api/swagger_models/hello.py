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


class HelloModelPost(Schema):
    type = 'object'
    properties = {
        'name': {
            'type': 'string'
        }
    }
    required = ['name']


class HelloModelPut(Schema):
    type = 'object'
    properties = {
        'name': {
            'type': 'string'
        }
    }
    required = ['name']


class HelloErrorModel(Schema):
    type = 'object'
    properties = {
        'error_code': {
            'type': 'string'
        },
        'error_message': {
            'type': 'string'
        }        
    }
    required = ['name']
    

from flask_restful_swagger_2 import Schema
from qube.src.api.swagger_models.hello import HelloModel, HelloModelPost, HelloErrorModel

"""
the common response messages printed in swagger UI
"""

post_response_msgs = {
    '201': {
        'description': 'CREATED',
        'schema': {"type": "string"}
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
        'description': 'Internal server error',
        'schema': HelloErrorModel        
    }
}

get_response_msgs = {
    '200': {
        'description': 'OK',
        'schema': HelloModel
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
        'description': 'Internal server error',
        'schema': HelloErrorModel        
    }
}

put_response_msgs = {
    '202': {
        'description': 'ACCEPTED',
        'schema': HelloModel
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
        'description': 'Internal server error',
        'schema': HelloErrorModel
    }
}

del_response_msgs = {
    '202': {
        'description': 'ACCEPTED'
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
        'description': 'Internal server error',
        'schema': HelloErrorModel
    }
}



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

#!/usr/bin/python
"""
Add docstring here
"""
from flask.ext.restful_swagger_2 import Resource, swagger
from flask_restful import reqparse
from qube.src.api.swagger_models.parameters \
    import header_ex, path_ex, query_ex
from qube.src.api.swagger_models.response_messages \
    import response_msgs
from qube.src.commons.log import Log as LOG
from flask import  request
from qube.src.models.hello import Hello


params = [header_ex, path_ex, query_ex]


class HelloItemResource(Resource):
    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world get operation',
            'parameters': params,
            'responses': response_msgs
        }
    )
    def get(self, id):
        LOG.debug("hello world")

        parser = reqparse.RequestParser()
        #parser.add_argument('id')
        args = parser.parse_args()
        data = Hello.query.get(id)
        hello_data = data.wrap()

        #normalize the name for 'id'
        if '_id' in hello_data:
            hello_data['id'] = str(hello_data['_id'])
            del hello_data['_id']

        return hello_data

        
    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world update toolchain operation',
            'responses': response_msgs
        }
    ) 
    def put(self, id):
        """
        Update.
        """
        # Validate request body with schema model
        hello_data = None


        try:
            #data = Hello(**request.get_json())
            data = request.get_json()
            #hello_data = Hello(data)
            old_hello = Hello.query.get(id)
            old_hello.update(data)
#             z.update(y)
#              z = 
            old_hello.save()
            return '', 204, {'Location': request.path + '/' + str(old_hello.mongo_id)}

        except e:
            return ErrorModel(**{'message': e.args[0]}), 400

     
        return 'unexpected error', 500

class HelloWorld(Resource):

    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world create toolchain operation',
            'responses': response_msgs
        }
    )

    def post(self):
        """
        Adds a hello item.
        """
        hello_data = None


        try:
            data = request.get_json()
            hello_data = Hello(name=data['name'])
            hello_data.save()

        except ValueError as e:
            return ErrorModel(**{'message': e.args[0]}), 400

        if hello_data:
            return '', 201, {'Location': request.path + '/' + str(hello_data.mongo_id)}
        else:
            return 'unexpected error', 500
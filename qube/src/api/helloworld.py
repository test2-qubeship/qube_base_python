#!/usr/bin/python
"""
Add docstring here
"""
from flask_restful_swagger_2 import Resource, swagger
from flask_restful import reqparse
from qube.src.api.swagger_models.parameters \
    import header_ex, path_ex, query_ex, body_ex
from qube.src.api.swagger_models.response_messages \
    import response_msgs, ErrorModel
from qube.src.commons.log import Log as LOG
from flask import  request
from qube.src.models.hello import Hello
from qube.src.api.swagger_models.hello import HelloModel
from qube.src.commons.utils import clean_nonserializable_attributes
import json


hello_item_get_params = [header_ex, path_ex, query_ex]
hello_item_put_params = [header_ex, path_ex, body_ex]
hello_post_params = [header_ex, path_ex, body_ex]

class HelloItemResource(Resource):
    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world get operation',
            'parameters': hello_item_get_params,
            'responses': response_msgs
        }
    )
    def get(self, id=None):
        LOG.debug("hello world")

        parser = reqparse.RequestParser()
        data = Hello.query.get(id)
        hello_data = data.wrap()
        clean_nonserializable_attributes(hello_data)
        return HelloModel(**hello_data)

    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world put operation',
            'parameters': hello_item_put_params,
            'responses': response_msgs
        }
    )
    def put(self, id):
        try:
            hello_model = HelloModel(**request.get_json())
            hello_record = Hello.query.get(id)
            merged_hello_record = hello_record.wrap()
            merged_hello_record.update(hello_model)
            updated_hello_record = Hello.unwrap(merged_hello_record)
            updated_hello_record.save()
            return '', 200, {'Location': request.path + '/' + str(updated_hello_record.mongo_id)}
        except ValueError as e:
            LOG.error(e)
            return ErrorModel(**{'message': e.args[0]}), 400
        except Exception as ex:
            LOG.error(ex)
            return ErrorModel(**{'message': ex.args[0]}), 500



class HelloWorld(Resource):

    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world create toolchain operation',
            'parameters' : hello_post_params,
            'responses': response_msgs
        }
    )

    def post(self):
        """
        Adds a hello item.
        """
        hello_data = None
        try:
            hello_model = HelloModel(**request.get_json())
            #data = request.get_json()
            hello_data = Hello.unwrap (hello_model)
            #hello_data = Hello(name=data['name'])
            hello_data.save()
            return '', 201, {'Location': request.path + '/' + str(hello_data.mongo_id)}
        except ValueError as e:
            LOG.error(e)
            return ErrorModel(**{'message': e.args[0]}), 400
        except Exception as ex:
            LOG.error(ex)
            return ErrorModel(**{'message': ex.args[0]}), 500
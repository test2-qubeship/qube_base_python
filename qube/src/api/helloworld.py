#!/usr/bin/python
"""
Add docstring here
"""
from flask import request
from flask_restful_swagger_2 import Resource, swagger
from mongoalchemy.exceptions import ExtraValueException

from qube.src.api.decorators import login_required
from qube.src.api.swagger_models.hello import *
from qube.src.api.swagger_models.parameters import (
    header_ex, path_ex, query_ex, body_post_ex, body_put_ex)
from qube.src.api.swagger_models.response_messages import (
    post_response_msgs, get_response_msgs,
    put_response_msgs, del_response_msgs, ErrorModel)
from qube.src.commons.error import HelloServiceError
from qube.src.commons.log import Log as LOG
from qube.src.commons.utils import clean_nonserializable_attributes
from qube.src.services.helloservice import HelloService

hello_item_get_params = [header_ex, path_ex, query_ex]
hello_item_put_params = [header_ex, path_ex, body_put_ex]
hello_item_delete_params = [header_ex, path_ex]
hello_get_params = [header_ex]
hello_post_params = [header_ex, body_post_ex]


class HelloItemResource(Resource):
    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world get operation',
            'parameters': hello_item_get_params,
            'responses': get_response_msgs
        }
    )
    @login_required
    def get(self, authcontext, entity_id):
        """gets an hello item that omar has changed
        """
        try:
            LOG.debug("hello world")
            hello_data = HelloService(authcontext['context'])\
                .find_hello_by_id(entity_id)
            clean_nonserializable_attributes(hello_data)
        except HelloServiceError as e:
            LOG.error(e)
            return ErrorModel(**{'message': e.args[0]}), e.errors
        except ValueError as e:
            LOG.error(e)
            return ErrorModel(**{'message': e.args[0]}), 400
        return HelloModel(**hello_data), 200

    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world put operation',
            'parameters': hello_item_put_params,
            'responses': put_response_msgs
        }
    )
    @login_required
    def put(self, authcontext, entity_id):
        """
        updates an hello item
        """
        try:
            hello_model = HelloModelPut(**request.get_json())
            context = authcontext['context']
            HelloService(context).update_hello(hello_model, entity_id)
            return '', 204
        except HelloServiceError as e:
            LOG.error(e)
            return ErrorModel(**{'message': e.args[0]}), e.errors
        except ValueError as e:
            LOG.error(e)
            return ErrorModel(**{'message': e.args[0]}), 400
        except Exception as ex:
            LOG.error(ex)
            return ErrorModel(**{'message': ex.args[0]}), 500

    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world delete operation',
            'parameters': hello_item_delete_params,
            'responses': del_response_msgs
        }
    )
    @login_required
    def delete(self, authcontext, entity_id):
        """
        Delete hello item
        """
        try:
            HelloService(authcontext['context']).delete_hello(entity_id)
            return '', 204
        except HelloServiceError as e:
            LOG.error(e)
            return ErrorModel(**{'message': e.args[0]}), e.errors
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
            'description': 'hello world get operation',
            'parameters': hello_get_params,
            'responses': get_response_msgs
        }
    )
    @login_required
    def get(self, authcontext):
        """
        gets all hello items
        """
        LOG.debug("Serving  Get all request")
        hello_list = HelloService(authcontext['context']).get_all_hellos()
        # normalize the name for 'id'
        return hello_list, 200

    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world create operation',
            'parameters': hello_post_params,
            'responses': post_response_msgs
        }
    )
    @login_required
    def post(self, authcontext):
        """
        Adds a hello item.
        """
        try:
            hello_model = HelloModelPost(**request.get_json())
            hello_result = HelloService(authcontext['context'])\
                .save_hello(hello_model)

            response = HelloModelPostResponse()
            for key in response.properties:
                response[key] = hello_result[key]

            return (response, 201,
                    {'Location': request.path + '/' + str(response['id'])})
        except ValueError as e:
            LOG.error(e)
            return ErrorModel(**{'message': e.args[0]}), 400
        except ExtraValueException as e:
            LOG.error(e)
            return ErrorModel(**{'message': "{} is not valid input".
                              format(e.args[0])}), 400
        except Exception as ex:
            LOG.error(ex)
            return ErrorModel(**{'message': ex.args[0]}), 500

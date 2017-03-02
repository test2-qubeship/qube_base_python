#!/usr/bin/python
"""
Add docstring here
"""
from flask import request
from flask_restful_swagger_2 import Resource, swagger
from mongoalchemy.exceptions import ExtraValueException

from qube.src.api.decorators import login_required
from qube.src.api.swagger_models.hello import HelloModel, VersionModel  # noqa: ignore=I100
from qube.src.api.swagger_models.hello import HelloModelPost # noqa: ignore=I100
from qube.src.api.swagger_models.hello import HelloModelPostResponse # noqa: ignore=I100
from qube.src.api.swagger_models.hello import HelloModelPut # noqa: ignore=I100

from qube.src.api.swagger_models.parameters import (
    body_post_ex, body_put_ex, header_ex, path_ex, query_ex)
from qube.src.api.swagger_models.response_messages import (
    del_response_msgs, ErrorModel, get_response_msgs, post_response_msgs,
    put_response_msgs, response_msgs)
from qube.src.commons.error import HelloServiceError
from qube.src.commons.log import Log as LOG
from qube.src.commons.utils import clean_nonserializable_attributes
from qube.src.services.helloservice import HelloService
from src.commons.qube_config import QubeConfig

EMPTY = ''
get_details_params = [header_ex, path_ex, query_ex]
put_params = [header_ex, path_ex, body_put_ex]
delete_params = [header_ex, path_ex]
get_params = [header_ex]
post_params = [header_ex, body_post_ex]


class ResourceItemVersionController(Resource):
    def __init__(self, *args, **kwargs):
        super(ResourceItemVersionController, self).__init__(*args, **kwargs)
        self.config = QubeConfig.get_config()

    @swagger.doc(
        {
            'tags': ['Hello'],
            'description': 'Hello Version operation',
            'responses': response_msgs
        }
    )
    def get(self):
        """gets an hello item that omar has changed
        """
        try:
            LOG.debug("Get version ")
            return VersionModel(**{'version': self.config.get_version()}), 200
        except Exception as ex:
            LOG.error(ex)
            return ErrorModel(**{'message': ex}), 500

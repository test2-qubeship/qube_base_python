#!/usr/bin/python
"""
Add docstring here
"""
from logging.config import fileConfig
import os

from flask import Flask

from flask_restful_swagger_2 import Api
from flask_swagger_ui import get_swaggerui_blueprint

from pkg_resources import resource_filename
from qube.src.api.helloworld import HelloWorld
from qube.src.commons.log import Log as LOG


logging_config = resource_filename(
    'qube.src.resources', 'logging_config.ini')
fileConfig(logging_config)

app = Flask(__name__)
API_URL = '/specs' # Our API url (can of course be a local resource)

api = Api(app, api_version='0.1', api_spec_url=API_URL)
DEFAULT_HOST = os.environ['DEFAULT_LISTENER_HOST']
DEFAULT_PORT = int(os.environ.get('DEFAULT_LISTENER_PORT', '5000'))
DEBUG = os.environ.get('DEBUG', 'False') \
    in ("yes", "y", "true", "True", "t", "1")

api.add_resource(HelloWorld, '/hello')

SWAGGER_URL = '/api/docs' # URL for exposing Swagger UI (without trailing '/')

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
  SWAGGER_URL, # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
  API_URL,
  #config={ # Swagger UI config overrides
  #'supportedSubmitMethods': ['get']
  #}
)

# Register blueprint at URL
# (URL must match the one given to factory function above)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


def main():
    """ main
    """
    app.secret_key = os.urandom(24)
    LOG.info("starting app...")
    app.run(debug=DEBUG,
            host=DEFAULT_HOST,
            port=DEFAULT_PORT)


if __name__ == '__main__':
    main()

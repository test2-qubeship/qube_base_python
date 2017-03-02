#!/usr/bin/python
"""
Add docstring here
"""
import io
import json
import os
import unittest
from mock import patch
import mongomock
from qube.src.commons import qube_config
from pkg_resources import resource_filename

from src.commons.qube_config import QubeConfig

HELLO_VERSION = "/v1/hello/version"
with patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient):
    os.environ['QUBE_SERVICE_MONGOALCHEMY_CONNECTION_STRING'] = ''
    os.environ['QUBE_SERVICE_MONGOALCHEMY_SERVER'] = ''
    os.environ['QUBE_SERVICE_MONGOALCHEMY_PORT'] = ''
    os.environ['QUBE_SERVICE_MONGOALCHEMY_DATABASE'] = ''
    from qube.src.api.app import app


class TestHelloVersionController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setup")

    def setUp(self):
        self.test_client = app.test_client()

    def tearDown(self):
        print("teardown")

    def test_hello_default_version(self, *args, **kwargs):
        QubeConfig.QUBE_VERSION_FILE = resource_filename(
            'qube.src.resources', 'qube_version_dontexist.txt')
        QubeConfig.get_config().version_str = None
        rv = self.test_client.get(HELLO_VERSION,
                                  headers=[('Content-Type',
                                            'application/json')])
        result = json.loads(rv.data.decode('utf-8'))
        self.assertTrue(rv._status_code == 200)
        self.assertEquals(result['version'], qube_config.DEFAULT_VERSION)

    def test_hello_git_version(self, *args, **kwargs):
        QubeConfig.QUBE_VERSION_FILE = resource_filename(
            'qube.src.resources', 'qube_sample_version.txt')
        QubeConfig.get_config().version_str = None
        with open(QubeConfig.QUBE_VERSION_FILE, 'r') as f:
            expected_version_str_file = f.read()

        expected_version_string = "{} ({})". \
            format(qube_config.DEFAULT_VERSION, expected_version_str_file.strip())

        rv = self.test_client.get(HELLO_VERSION,
                                  headers=[('Content-Type',
                                            'application/json')])
        result = json.loads(rv.data.decode('utf-8'))
        self.assertTrue(rv._status_code == 200)
        self.assertEquals(result['version'], expected_version_string)

    @classmethod
    def tearDownClass(cls):
        print("After class")


if __name__ == '__main__':
    unittest.main()

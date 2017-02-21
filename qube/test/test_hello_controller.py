#!/usr/bin/python
"""
Add docstring here
"""
import io
import json
import os
import time
import unittest

import mongomock
from mock import patch

# noinspection PyUnresolvedReferences
with patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient):
    os.environ['MONGOALCHEMY_CONNECTION_STRING'] = ''
    os.environ['MONGOALCHEMY_SERVER'] = ''
    os.environ['MONGOALCHEMY_PORT'] = ''
    os.environ['MONGOALCHEMY_DATABASE'] = ''
    from qube.src.api import app  # import app.py
    from qube.src.api.app import *
    from qube.src.models.hello import Hello


def auth_response():
    userinfo = {
        'id': '1009009009988',
        'type': 'org',
        'tenant': {
            'id': '23432523452345',
            'orgs': [{
                'id': '987656789765670'
            }]
        }
    }

    return json.dumps(userinfo)


def invalid_auth_response():
    userinfo = {
        'id': '1009009009988',
        'type': 'master',
        'tenant': {
            'id': '23432523452345',
            'orgs': [{
                'id': '987656789765670'
            }]
        }
    }
    return json.dumps(userinfo)


def no_auth_response():
    userinfo = {
    }

    return json.dumps(userinfo)


class TestHelloController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("before class")

    def createTestModelData(self):
        return {'name': 'test123123124'}

    def createTestHeaders(self, data):
        headers = [('Content-Type', 'application/json'),
                   ('Authorization', 'Bearer authorizationmockedvaluedoesntmatter')]
        if data is not None:
            json_data = json.dumps(data)
            json_data_length = len(json_data)
            headers.append(('Content-Length', str(json_data_length)))
        return headers

    @patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setupDatabaseRecords(self):
        with patch('mongomock.write_concern.WriteConcern.__init__', return_value=None):
            hello_data = Hello(name='test_record')
            hello_data.tenantId = "23432523452345"
            hello_data.orgId = "987656789765670"
            hello_data.createdBy = "1009009009988"
            hello_data.modifiedBy = "1009009009988"
            hello_data.createDate = str(int(time.time()))
            hello_data.modifiedDate = str(int(time.time()))
            hello_data.save()
            return hello_data

    @patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setUp(self):
        self.hello_data = self.setupDatabaseRecords()
        self.hello_model_data = self.createTestModelData()
        self.hello_headers = self.createTestHeaders(self.hello_model_data)
        self.auth = auth_response()
        self.test_client = app.test_client()

    def tearDown(self):
        with patch('mongomock.write_concern.WriteConcern.__init__', return_value=None):
            self.hello_data.remove()

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    @patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(auth_response(), 200))
    def test_post_hello(self, *args, **kwargs):
        rv = self.test_client.post("/hello", input_stream=io.BytesIO(json.dumps(self.hello_model_data)),
                                   headers=self.hello_headers)
        print rv.status
        result = json.loads(rv.data)

        self.assertTrue(rv._status_code == 201)
        Hello.query.get(result['id']).remove()

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    @patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(auth_response(), 200))
    def test_put_hello_item(self, *args, **kwargs):
        entity_id = str(self.hello_data.mongo_id)
        self.hello_model_data['desc'] = 'updated model desc'
        rv = self.test_client.put("/hello/{}".format(entity_id),
                                  input_stream=io.BytesIO(json.dumps(self.hello_model_data)),
                                  headers=self.hello_headers)
        self.assertTrue(rv._status_code == 204)
        updated_hello_record = Hello.query.get(entity_id)
        self.assertEquals(self.hello_model_data['desc'], updated_hello_record.desc)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    @patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(auth_response(), 200))
    def test_put_hello_item_non_found(self, *args, **kwargs):
        rv = self.test_client.put("/hello/{}".format(1234), input_stream=io.BytesIO(json.dumps(self.hello_model_data)),
                                  headers=self.hello_headers)
        print rv.status
        self.assertTrue(rv._status_code == 404)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    @patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(auth_response(), 200))
    def test_get_hello(self, *args, **kwargs):
        id_to_get = str(self.hello_data.mongo_id)
        rv = self.test_client.get("/hello", headers=self.hello_headers)
        print rv.status
        result_collection = json.loads(rv.data)
        self.assertTrue(rv._status_code == 200)
        self.assertTrue(len(result_collection) == 1)
        self.assertTrue(result_collection[0].get('id') == id_to_get)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    @patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(auth_response(), 200))
    def test_get_hello_item(self, *args, **kwargs):
        id_to_get = str(self.hello_data.mongo_id)
        rv = self.test_client.get("/hello/{}".format(id_to_get), headers=self.hello_headers)
        result = json.loads(rv.data)
        self.assertTrue(rv._status_code == 200)
        self.assertTrue(id_to_get == result['id'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    @patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(auth_response(), 200))
    def test_get_hello_item_not_found(self, *args, **kwargs):
        rv = self.test_client.get("/hello/{}".format(12345), headers=self.hello_headers)
        self.assertTrue(rv._status_code == 404)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    @patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(auth_response(), 200))
    def test_delete_hello_item(self, *args, **kwargs):
        id_to_delete = str(self.hello_data.mongo_id)
        rv = self.test_client.delete("/hello/{}".format(id_to_delete), headers=self.hello_headers)
        self.assertTrue(rv._status_code == 204)
        deleted_hello_record = Hello.query.get(id_to_delete)
        self.assertIsNone(deleted_hello_record)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    @patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(auth_response(), 200))
    def test_delete_hello_item_notfound(self, *args, **kwargs):
        rv = self.test_client.delete("/hello/{}".format(123456), headers=self.hello_headers)
        self.assertTrue(rv._status_code == 404)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    @patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(no_auth_response(), 401))
    def test_get_hello_not_authorized(self, *args, **kwargs):
        rv = self.test_client.get("/hello", headers=self.hello_headers)
        print rv.status
        self.assertTrue(rv._status_code == 401)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    @patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(invalid_auth_response(), 200))
    def test_get_hello_master_token(self, *args, **kwargs):
        rv = self.test_client.get("/hello", headers=self.hello_headers)
        self.assertTrue(rv._status_code == 403)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    @patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(no_auth_response(), 401))
    def test_get_hello_no_authorization(self, *args, **kwargs):
        rv = self.test_client.get("/hello", headers=[('Content-Type', 'application/json')])
        print rv.status
        self.assertTrue(rv._status_code == 401)

    @classmethod
    def tearDownClass(cls):
        print("After class")


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/python
"""
Add docstring here
"""
import os
import time
import unittest

import mock
from mock import patch
import mongomock


with patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient):
    os.environ['QUBE_SERVICE_MONGOALCHEMY_CONNECTION_STRING'] = ''
    os.environ['QUBE_SERVICE_MONGOALCHEMY_SERVER'] = ''
    os.environ['QUBE_SERVICE_MONGOALCHEMY_PORT'] = ''
    os.environ['QUBE_SERVICE_MONGOALCHEMY_DATABASE'] = ''

    from qube.src.models.hello import Hello
    from qube.src.services.helloservice import HelloService
    from qube.src.commons.context import AuthContext
    from qube.src.commons.error import HelloServiceError


class TestHelloService(unittest.TestCase):
    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setUp(self):
        context = AuthContext("23432523452345", "987656789765670",
                                                "1009009009988")
        self.helloService = HelloService(context)
        self.hello_data = self.setupDatabaseRecords()
        self.hello_api_model = self.createTestModelData()
        self.hello_api_model_put_description \
            = self.createTestModelDataDescription()

    def tearDown(self):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            self.hello_data.remove()

    def createTestModelData(self):
        return {'name': 'test123123124'}

    def createTestModelDataDescription(self):
        return {'desc': 'test123123124'}

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setupDatabaseRecords(self):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            hello_data = Hello(name='test_record')
            hello_data.desc = 'my short description'
            hello_data.tenantId = "23432523452345"
            hello_data.orgId = "987656789765670"
            hello_data.createdBy = "1009009009988"
            hello_data.modifiedBy = "1009009009988"
            hello_data.createDate = str(int(time.time()))
            hello_data.modifiedDate = str(int(time.time()))
            hello_data.save()
            return hello_data

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_post_hello(self, *args, **kwargs):
        result = self.helloService.save(self.hello_api_model)
        self.assertTrue(result['id'] is not None)
        self.assertTrue(result['name'] == self.hello_api_model['name'])
        Hello.query.get(result['id']).remove()

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_hello(self, *args, **kwargs):
        self.hello_api_model['name'] = 'modified for put'
        id_to_find = str(self.hello_data.mongo_id)
        result = self.helloService.update(
            self.hello_api_model, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['name'] == self.hello_api_model['name'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_hello_description(self, *args, **kwargs):
        self.hello_api_model_put_description['desc'] = 'modified for put'
        id_to_find = str(self.hello_data.mongo_id)
        result = self.helloService.update(
            self.hello_api_model_put_description, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['desc'] ==
                        self.hello_api_model_put_description['desc'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_hello_item(self, *args, **kwargs):
        id_to_find = str(self.hello_data.mongo_id)
        result = self.helloService.find_by_id(id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_hello_item(self, *args, **kwargs):
        id_to_delete = str(self.hello_data.mongo_id)
        self.helloService.delete(id_to_delete)
        with self.assertRaises(HelloServiceError):
            self.helloService.find_by_id(id_to_delete)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_hello_item_invalid(self, *args, **kwargs):
        id_to_find = '123notexist'
        with self.assertRaises(HelloServiceError):
            self.helloService.find_by_id(id_to_find)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_hello_list(self, *args, **kwargs):
        result_collection = self.helloService.get_all()
        self.assertTrue(len(result_collection) == 1)
        self.assertTrue(result_collection[0]['id'] ==
                        str(self.hello_data.mongo_id))

#!/usr/bin/python
"""
Add docstring here
"""
import os
import unittest
import mongomock
from mock import patch
import json
import io
import time
from mock import MagicMock


with patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient):
    from qube.src.api import app # import app.py
    import qube.src.api.app      # import app from module (__init__)
    from qube.src.models.hello import Hello


class TestHelloController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        print("before class")

    @staticmethod
    def createTestData():
        return {'name': 'test123123124'}

    @staticmethod
    def userinfo():
        userinfo = {
            'id': '1009009009988',
            'type': 'org',
            'tenant':{
                'id':'23432523452345',
                'orgs':[{
                    'id':'987656789765670'
                }]
            }
        }

        return json.dumps(userinfo)

    @staticmethod
    def createTestHeaders(data):
        headers = [('Content-Type', 'application/json'),('Authorization','Bearer authorizationmockedvaluedoesntmatter')]
        if(data is not None):
            json_data = json.dumps(data)
            json_data_length = len(json_data)
            headers.append(('Content-Length', json_data_length))
        return headers

    def test_post_hello(self):

        with app.test_client() as c:
            data = self.createTestData()
            headers = self.createTestHeaders(data)
            with patch('mongomock.write_concern.WriteConcern.__init__',return_value=None):
                with patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(self.userinfo(),200)):
                    rv = c.post("/hello",input_stream=io.BytesIO(json.dumps(data)), headers=headers)
                    print rv.status
                    self.assertTrue(rv._status_code == 201)

    def test_put_hello_item(self):
        with patch('mongomock.write_concern.WriteConcern.__init__', return_value=None):
            hello_data = Hello(name='test_record')
            hello_data.tenantId = "23432523452345"
            hello_data.orgId = "987656789765670"
            hello_data.createdBy = "1009009009988"
            hello_data.modifiedBy = "1009009009988"
            hello_data.createDate = str(int(time.time()))
            hello_data.modifiedDate = str(int(time.time()))
            hello_data.save()
            with app.test_client() as c:
                data = self.createTestData()
                headers = self.createTestHeaders(data)
                with patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(self.userinfo(),200)):
                    rv = c.put("/hello/"+str(hello_data.mongo_id),input_stream=io.BytesIO(json.dumps(data)), headers=headers)
                    print rv.status
                    self.assertTrue(rv._status_code == 204)
                #updated_record = Hello.query.get(hello_data.mongo_id)
                #self.assertTrue(updated_record.name  == services ['name'])

    def test_put_hello_item_non_found(self):
        with patch('mongomock.write_concern.WriteConcern.__init__', return_value=None):
            with app.test_client() as c:
                data = self.createTestData()
                headers = self.createTestHeaders(data)
                with patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(self.userinfo(),200)):
                    rv = c.put("/hello/1234",input_stream=io.BytesIO(json.dumps(data)), headers=headers)
                    print rv.status
                    self.assertTrue(rv._status_code == 404)

    def test_get_hello(self):
        with patch('mongomock.write_concern.WriteConcern.__init__', return_value=None):
            hello_data = Hello(name='test_record')
            hello_data.tenantId = "23432523452345"
            hello_data.orgId = "987656789765670"
            hello_data.createdBy = "1009009009988"
            hello_data.modifiedBy = "1009009009988"
            hello_data.createDate = str(int(time.time()))
            hello_data.modifiedDate = str(int(time.time()))
            hello_data.save()
        with app.test_client() as c:
            headers = self.createTestHeaders(None)
            with patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(self.userinfo(),200)):
                rv = c.get("/hello", headers=headers)
                print rv.status
                result_collection = json.loads(rv.data)
                self.assertTrue(rv._status_code == 200)
                self.assertTrue(len(result_collection) == 1)

    def test_get_hello_item(self):
        with patch('mongomock.write_concern.WriteConcern.__init__', return_value=None):
            hello_data = Hello(name='test_record')
            hello_data.tenantId = "23432523452345"
            hello_data.orgId = "987656789765670"
            hello_data.createdBy = "1009009009988"
            hello_data.modifiedBy = "1009009009988"
            hello_data.createDate = str(int(time.time()))
            hello_data.modifiedDate = str(int(time.time()))
            hello_data.save()
            with app.test_client() as c:
                headers = self.createTestHeaders(None)
                with patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(self.userinfo(),200)):
                    rv = c.get("/hello/"+str(hello_data.mongo_id), headers=headers)
                    print rv.status
                    result = json.loads(rv.data)
                    self.assertTrue(rv._status_code == 200)
                    self.assertTrue(str(hello_data.mongo_id) == result['id'])

    def test_get_hello_item_not_found(self):
        with patch('mongomock.write_concern.WriteConcern.__init__', return_value=None):
            with app.test_client() as c:
                headers = self.createTestHeaders(None)
                with patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(self.userinfo(),200)):
                    rv = c.get("/hello/12345", headers=headers)
                    print rv.status
                    result = json.loads(rv.data)
                    self.assertTrue(rv._status_code == 404)

    def test_delete_hello_item(self):
        with patch('mongomock.write_concern.WriteConcern.__init__', return_value=None):
            hello_data = Hello(name='test_record')
            hello_data.tenantId = "23432523452345"
            hello_data.orgId = "987656789765670"
            hello_data.createdBy = "1009009009988"
            hello_data.modifiedBy = "1009009009988"
            hello_data.createDate = str(int(time.time()))
            hello_data.modifiedDate = str(int(time.time()))


            hello_data.save()
            with app.test_client() as c:
                headers = self.createTestHeaders(None)
                with patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(self.userinfo(),200)):
                    rv = c.delete("/hello/"+str(hello_data.mongo_id), headers=headers)
                    print rv.status
                    self.assertTrue(rv._status_code == 204)
                    deleted_hello_record = Hello.query.get(str(hello_data.mongo_id))
                    self.assertIsNone( deleted_hello_record)

    def test_delete_hello_item_notfound(self):
        with patch('mongomock.write_concern.WriteConcern.__init__', return_value=None):
            with app.test_client() as c:
                headers = self.createTestHeaders(None)
                with patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(self.userinfo(), 200)):
                    rv = c.delete("/hello/123456", headers=headers)
                    print rv.status
                    self.assertTrue(rv._status_code == 404)


    def test_get_hello_not_authorized(self):
        with app.test_client() as c:
            headers = self.createTestHeaders(None)
            with patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(None,401)):
                rv = c.get("/hello", headers=headers)
                print rv.status
                result_collection = json.loads(rv.data)
                self.assertTrue(rv._status_code == 401)

    def test_get_hello_master_token(self):
        with app.test_client() as c:
            headers = self.createTestHeaders(None)
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
            with patch('qube.src.api.decorators.validate_with_qubeship_auth', return_value=(json.dumps(userinfo),200)):
                rv = c.get("/hello", headers=headers)
                print rv.status
                result_collection = json.loads(rv.data)
                self.assertTrue(rv._status_code == 403)

    def test_get_hello_no_authorization(self):
        with app.test_client() as c:
            rv = c.get("/hello", headers= [('Content-Type', 'application/json')])
            print rv.status
            result_collection = json.loads(rv.data)
            self.assertTrue(rv._status_code == 401)

    @classmethod
    def tearDownClass(cls):
        print("After class")

if __name__ == '__main__':
    unittest.main()

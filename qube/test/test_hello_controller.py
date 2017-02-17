#!/usr/bin/python
"""
Add docstring here
"""
import os
import unittest
import mock
import mongomock
from mock import patch
import json
import io
import sys
from mock import MagicMock
#from qube.src.api import app

with patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient):
    from qube.src.api import app
    import qube.src.api.app
    from qube.src.models.hello import Hello

#app.config = MagicMock(return_value=None)
class TestHelloController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("before class")
        
    def test_post_hello(self):
        headers = [('Content-Type', 'application/json')]
        data = {'name': 'test123123124'}
        json_data = json.dumps(data)
        json_data_length = len(json_data)
        headers.append(('Content-Length', json_data_length))

        with app.test_client() as c:
             with patch('mongomock.write_concern.WriteConcern.__init__',return_value=None):
                 rv = c.post("/hello",input_stream=io.BytesIO(json.dumps(data)), headers=headers)
                 print rv.status
                 self.assertTrue(rv._status_code == 201)

    def test_put_hello_item(self):
        with patch('mongomock.write_concern.WriteConcern.__init__', return_value=None):
            hello_data = Hello(name='test_record')
            hello_data.save()
            with app.test_client() as c:
                headers = [('Content-Type', 'application/json')]
                data = {'name': 'test123123124'}
                json_data = json.dumps(data)
                json_data_length = len(json_data)
                headers.append(('Content-Length', json_data_length))
                rv = c.put("/hello/"+str(hello_data.mongo_id),input_stream=io.BytesIO(json.dumps(data)), headers=headers)
                print rv.status
                self.assertTrue(rv._status_code == 200)
                updated_record = Hello.query.get(hello_data.mongo_id)
                self.assertTrue(updated_record.name  == data ['name'])

    def test_get_hello(self):
        with patch('mongomock.write_concern.WriteConcern.__init__', return_value=None):
            hello_data = Hello(name='test_record')
            hello_data.save()
        with app.test_client() as c:
            headers = [('Content-Type', 'application/json')]
            rv = c.get("/hello", headers=headers)
            print rv.status
            result_collection = json.loads(rv.data)
            self.assertTrue(rv._status_code == 200)
            self.assertTrue(len(result_collection) == 1)


    def test_get_hello_item(self):
        with patch('mongomock.write_concern.WriteConcern.__init__', return_value=None):
            hello_data = Hello(name='test_record')
            hello_data.save()
            with app.test_client() as c:
                headers = [('Content-Type', 'application/json')]
                rv = c.get("/hello/"+str(hello_data.mongo_id), headers=headers)
                print rv.status
                result = json.loads(rv.data)
                self.assertTrue(rv._status_code == 200)
                self.assertTrue(str(hello_data.mongo_id) == result['id'])

    def test_delete_hello_item(self):
        with patch('mongomock.write_concern.WriteConcern.__init__', return_value=None):
            hello_data = Hello(name='test_record')
            hello_data.save()
            with app.test_client() as c:
                headers = [('Content-Type', 'application/json')]
                rv = c.delete("/hello/"+str(hello_data.mongo_id), headers=headers)
                print rv.status
                self.assertTrue(rv._status_code == 204)
                deleted_hello_record = Hello.query.get(str(hello_data.mongo_id))
                self.assertTrue( deleted_hello_record is None)


    @classmethod
    def tearDownClass(cls):
        print("After class")

if __name__ == '__main__':
    unittest.main()

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

#from qube.src.api import app

#app.config = MagicMock(return_value=None)
class TestHelloController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("before class")
        
    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def test_post_hello(self):
        from qube.src.api import app
        import qube.src.api.app
        from qube.src.models.hello import Hello
        from qube.src.api.helloworld import HelloWorld

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


    @classmethod
    def tearDownClass(cls):
        print("After class")

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/python
"""
Add docstring here
"""
import os
import unittest
import mock
import mongomock
from mock import patch

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
        
        #with patch('flask.request.get_json', return_value=test):
        #     hello_world = HelloWorld()
        #     msg,code,headers = hello_world.post();
        #     self.assertTrue(code=200)    
        with app.test_client() as c:
             with patch('mongomock.write_concern.WriteConcern.__init__',return_value=None):
                 rv= c.post("/hello",input_stream=open('/Users/veeren/Documents/CA/qubeship/qube_base_python/qube/test/input','r'),headers={'content-type':'application/json'})
                 print rv.status 
                 self.assertTrue(rv.status == 200)
             

    @classmethod
    def tearDownClass(cls):
        print("After class")

if __name__ == '__main__':
    unittest.main()

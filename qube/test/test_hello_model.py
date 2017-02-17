#!/usr/bin/python
"""
Add docstring here
"""
import unittest
import mock
import mongomock
from mock import patch


class TestHelloModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("before class")
        
    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def test_create_hello_model(self):
        from qube.src.models.hello import Hello
        hello_data = Hello(name='testname')
        with patch('mongomock.write_concern.WriteConcern.__init__',return_value=None):
            hello_data.save()
        
        self.assertIsNotNone(hello_data.mongo_id)

    @classmethod
    def tearDownClass(cls):
        print("After class")

if __name__ == '__main__':
    unittest.main()

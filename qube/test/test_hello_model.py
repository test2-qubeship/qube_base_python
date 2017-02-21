#!/usr/bin/python
"""
Add docstring here
"""
import unittest
import mock
import mongomock
from mock import patch
import time


class TestHelloModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("before class")
        
    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def test_create_hello_model(self):
        from qube.src.models.hello import Hello
        hello_data = Hello(name='testname')
        hello_data.tenantId="23432523452345"
        hello_data.orgId = "987656789765670"
        hello_data.createdBy="1009009009988"
        hello_data.modifiedBy = "1009009009988"
        hello_data.createDate=str(int(time.time()))
        hello_data.modifiedDate = str(int(time.time()))
        with patch('mongomock.write_concern.WriteConcern.__init__',return_value=None):
            hello_data.save()
            self.assertIsNotNone(hello_data.mongo_id)
            hello_data.remove()

    @classmethod
    def tearDownClass(cls):
        print("After class")

if __name__ == '__main__':
    unittest.main()

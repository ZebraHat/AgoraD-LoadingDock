__author__ = 'chase'


#
## tests.py
## unit tests for the highway
#


from django.test import TestCase
from django.test.client import Client
import random


class TestHighway(TestCase):
    def test_transfer_start(self):
        client = Client()

        data = dict()
        data['token'] = None
        data['table_names'] = []
        data['destination'] = 'localhost'
        data['session_id'] = random.randint(0, 9999999)
        data['database_name'] = 'test_sqlite'

        response = client.post(path='/highway/transfer/start/', data=data)
        
        self.assertEqual(response.code, 200, msg='Transferring threw an error!')

        #TODO run more tests

    def test_transfer_schema(self):
        client = Client()

        data = dict()
        data['token'] = None
        data['table_names'] = []
        data['session_id'] = random.randint(0, 9999)
        data['database_name'] = 'qwertydb'

        response = client.post(path='/highway/transfer/schema', data=data)

        self.assertEqual(response.code, 200)

        #TODO assert schema inserts into the database

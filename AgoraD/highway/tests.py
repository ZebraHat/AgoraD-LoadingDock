__author__ = 'chase'


#
## tests.py
## unit tests for the highway
#


from django.test import TestCase
from django.test.client import Client
import random
from modules.blocks import *
from autofixture import AutoFixture
from test_app.models import Food, Food_Type, Student


class TestTransfer(TestCase):
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

    def test_intercept_schema(self):
        pass

    def test_intercept_block(self):
        pass


class TestBlockCreation(TestCase):
    def test_block_creation(self):
        ## load auto fixtures ##
        food_fixture = AutoFixture(Food, generate_fk=True)
        student_fixture = AutoFixture(Student, generate_fk=True)

        blocks = create_blocks('test_app_postgresql')
        print len(blocks)

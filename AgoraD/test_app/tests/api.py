__author__ = 'chase'

#
## tests.py
## unit tests for the highway
#


from django.test import TestCase
from django.test.client import Client
from fake_database import seed_database


class TestHighway(TestCase):
    def test_transfer_start(self):
        client = Client()

        seed_database('sqlite')
        seed_database('postgres')
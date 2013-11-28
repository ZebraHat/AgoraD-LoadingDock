__author__ = 'chase'


#
## tests.py
## unit tests for the highway
#


from django.test import TestCase
from django.test.client import Client


class TestHighway(TestCase):
    def test_transfer_start(self):
        client = Client()
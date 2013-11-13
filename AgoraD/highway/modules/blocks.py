#
## blocks.py
## Methods for breaking the database up into blocks
#
__author__ = 'chase'


import loading_dock.ModelGenerator
from loading_dock.models import Database, Tables, Column


def create_blocks():
    # look up database
    # iterate over tables and calc number of rows in each
    # break each table into segments of no more than 1000 rows
    # create block object

    ## grab a list of all databases, only support first for now
    database = Database.objects.all()[0]
    tables = Tables.objects.get(db=database)
    for table in tables:
        pass

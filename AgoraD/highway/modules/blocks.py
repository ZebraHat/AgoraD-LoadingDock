#
## blocks.py
## Methods for breaking the database up into blocks
#
__author__ = 'chase'


import loading_dock.ModelGenerator
from loading_dock.models import Database, Table, Column
from highway.models import Block


def create_blocks():
    # look up database
    # iterate over tables and calc number of rows in each
    # break each table into segments of no more than 1000 rows
    # create block object

    ## grab a list of all databases, only support first for now

    block_size = 1000

    database = Database.objects.all()[0]
    tables = Table.objects.filter(db=database)
    for table in tables:
        num_rows = table.objects.count()
        for x in range(0, num_rows, block_size):
            Block.objects.create(
                database=database,
                table=table,
                start_row=x,
                end_row=x + block_size - 1
            )
        ## do the last few blocks
        if num_rows % block_size:
            Block.objects.create(
                database=database,
                table=table,
                start_row=num_rows - num_rows % block_size,
                end_row=num_rows - 1
            )

        pass

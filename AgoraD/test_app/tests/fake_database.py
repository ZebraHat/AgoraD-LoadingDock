__author__ = 'chase'

from test_app.models import Person, Place


def seed_database(database_type):
    for x in range(10):
        Person.objects.create(
            first_name=database_type + '-first_name' + str(x),
            last_name=database_type + '-last_name' + str(x),
            email_address='{}@{}.com'.format(x, database_type)
        )

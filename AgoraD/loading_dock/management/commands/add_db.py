#
## add_db.py
## manage.py commands for adding a db to the auto generated models
#


from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connections, IntegrityError
from loading_dock.models import Database, Table, Column
from optparse import make_option

from django.utils import six

class Command(BaseCommand):
    args = '<dbname ...>'
    option_list = BaseCommand.option_list + (
            make_option('-t', '--table',
                action='append',
                dest='tables',
                help='Select tables to add'
                ),
            )
    help = 'Sets up new data stores listed in settings.py'

    def handle(self, *args, **options):
        if len(args) == 0:
            print 'Usage: python manage.py add_db <dbname ...>'
            print 'Possible dbnames: '
            for db in connections:
                if db == 'default':
                    continue
                print db

        if options['tables'] is not None:
            dbname = args[0]
            if dbname not in connections:
                print 'Not a valid database'
                return

            cursor = connections[dbname].cursor()
            introspector = connections[dbname].introspection

            db = Database.objects.get(name=dbname)

            for tablename in options['tables']:
                try:
                    table = _add_table(db, tablename)
                    type_reverser = _type_reverser(introspector, cursor, tablename)
                    for fieldinfo in introspector.get_table_description(cursor, tablename):
                        _add_column(table, fieldinfo, type_reverser)
                except IntegrityError:
                    print tablename + ' is not a valid table name.'

        else:
            for dbname in args:
                cursor = connections[dbname].cursor()
                introspector = connections[dbname].introspection
                type_reverser = introspector.data_types_reverse

                try:
                    db = _add_db(dbname)
                except IntegrityError:
                    db = Database.objects.get(name=dbname)
                    print 'Database ' + dbname + ' already added'

                for tablename in introspector.get_table_list(cursor):
                    table = _add_table(db, tablename)
                    type_reverser = _type_reverser(introspector, cursor, tablename)

                    for fieldinfo in introspector.get_table_description(cursor, tablename):
                        _add_column(table, fieldinfo, type_reverser)


def _add_db(dbname):
    db = Database(name=dbname)
    db.save()
    return db

def _add_table(db, tablename):
    table = None
    try:
        table = Table(name=tablename, db=db)
        table.save()
    except IntegrityError:
        table = Table.objects.get(name=tablename, db=db)
        for column in Column.objects.filter(table=table):
            column.delete()

    return table

def _add_column(table, columninfo, type_reverser):
    column = Column(table=table, name=columninfo[0], type=type_reverser(columninfo))
    column.save()
    return column

def _type_reverser(introspector, cursor, table):
    # for some reason, get_primary_key_column does not work,
    # but this code which does the exact same thing does.
    primary_key = None
    for column in six.iteritems(introspector.get_indexes(cursor, table)):
        print column
        if column[1]['primary_key']:
            primary_key = column[0]
    print introspector.get_primary_key_column(cursor, table)
    print primary_key
    def reverse(t):
        rt = introspector.get_field_type(t[1], t)
        if type(rt) is not tuple:
            rt = (rt, {})
        if str(t[0]) == primary_key:
            rt[1]['primary_key'] = True

        return rt

    return reverse

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connections, IntegrityError
from loading_dock.models import Database, Table, Column
from optparse import make_option

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
      print 'Usage: python manage.py adddb <dbname ...>'
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
          for fieldinfo in introspector.get_table_description(cursor, tablename):
            _add_column(table, fieldinfo)
        except IntegrityError:
          print tablename + ' is not a valid table name.'

    else:
      for dbname in args:
        cursor = connections[dbname].cursor()
        introspector = connections[dbname].introspection

        try:
          db = _add_db(dbname)
        except IntegrityError:
          print 'Database ' + dbname + ' already added'

        for tablename in introspector.get_table_list(cursor):
          table = _add_table(db, tablename)

          for fieldinfo in introspector.get_table_description(cursor, tablename):
            _add_column(table, fieldinfo)


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
    for column in Columns.objects.filter(table=table, db=db):
      column.delete()

  return table

def _add_column(table, columninfo):
  column = Column(table=table, name=columninfo[0], type=columninfo[1])
  column.save()
  return column


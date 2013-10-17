from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connections
from loading_dock.models import Database, Table, Column

class Command(BaseCommand):
  args = '<dbname ...>'
  help = 'Sets up new data stores listed in settings.py'

  def handle(self, *args, **options):
    if len(args) == 0:
      print 'Usage: python manage.py adddb <dbname ...>'
      print 'Possible dbnames: '
      for db in connections:
        if db == 'default':
          continue
        print db

    for dbname in args:
      cursor = connections[dbname].cursor()
      introspector = connections[dbname].introspection

      try:
        db = _add_db(dbname)
      except IntegrityError:
        print 'Database ' + dbname + ' already added'
        return

      for tablename in introspector.get_table_list(cursor):
        table = _add_table(db, tablename)
        
        for fieldinfo in introspector.get_table_description(cursor, tablename):
          _add_column(table, fieldinfo)

def _add_db(dbname):
  db = Database(name=dbname)
  db.save()
  return db

def _add_table(db, table):
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


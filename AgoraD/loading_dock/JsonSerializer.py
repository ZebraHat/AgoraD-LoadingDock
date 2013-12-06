#
## JsonSerializer.py
## functions for serializing and deserializing schemas
#


from django.db import connections
from models import Database, Table, Column
import json
import ModelGenerator
from django.core.serializers.json import DjangoJSONEncoder

def serialize(objects):
    json_objs = []
    for o in objects:
        obj = {}
        obj['class'] = o.__class__.__name__
        obj['fields'] = {}
        for f in o.__fields__:
            obj['fields'][f] = o.__dict__[f]

        json_objs.append(obj)

    return json.dumps(json_objs, cls=DjangoJSONEncoder)

def deserialize(json_str, destdb):
    json_objs = json.loads(json_str)
    objs = []

    for obj in json_objs:
        o = ModelGenerator.getModel(destdb, obj['class'])()
        for f, v in obj['fields'].iteritems():
            o.__dict__[f] = v

        objs.append(o)

    return objs

def schema2json(dbname = None, tablenames = None, destdb = None):
    """
    If no parameters are passed, creates a schema representation of
    all known databases and tables.
    If dbname is passed,
    creates a JSON representation of a table schema,
    using destdb as the database name if it is specified.
    """

    if dbname:
        dblist = [Database.objects.get(name=dbname)]
    else:
        dblist = Database.objects.all()

    schema = {}
    for db in dblist:
        if tablenames:
            tablelist = Table.objects.filter(db=db, name__in=tablenames)
        else:
            tablelist = Table.objects.filter(db=db)

        table_schema = {}
        for table in tablelist:
            table_schema[table.name] = {}

            for column in Column.objects.filter(table=table):
                table_schema[table.name][column.name] = column.type

        if destdb:
            schema[destdb] = table_schema
        else:
            schema[db.name] = table_schema

    return json.dumps(schema, sort_keys=True)

def json2schema(schema_json, commit = True, destdb = None):
    """
    Creates Database, Table, and Column objects as needed to satisfy the incoming schema.
    If the table is already present, assume we are updating: delete all columns and recreate from the schema.
    Unless commit is false, call the required sql to create the incoming tables in the destination database.
    """

    schema = json.loads(schema_json)

    for dbname, table_schema in schema.iteritems():
        if destdb:
            dbname = destdb

        try:
            db = Database.objects.get(name=dbname)
        except Database.DoesNotExist:
            db = Database(name=dbname)
            db.save()

        for tablename, column_schema in table_schema.iteritems():
            try:
                table = Table.objects.get(db=db, name=tablename)
                for column in Column.objects.filter(table=table):
                    column.delete()
            except Table.DoesNotExist:
                table = Table(db=db, name=tablename)
                table.save()

            for columnname, columntype in column_schema.iteritems():
                column = Column(table=table, name=columnname, type=columntype)
                column.save()

            if commit:
                model = ModelGenerator.getModel(dbname, tablename)
                cursor = connections[dbname].cursor()
                for sql in ModelGenerator.getSQL(model):
                    cursor.execute(sql)
    return None


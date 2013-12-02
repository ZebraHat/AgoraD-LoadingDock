from django.db import connections
from models import Database, Table, Column
import json
import ModelGenerator

def serialize(objects):
    json_objs = []
    for o in objects:
        obj = {}
        obj['class'] = o.__class__.__name__
        obj['fields'] = {}
        for f in o.__fields__:
            obj['fields'][f] = o.__dict__[f]

        json_objs.append(obj)

    return json.dumps(json_objs)

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
    creates a JSON representation of a table schema.
    Doesn't include the database name, because that's not guaranteed
    to be the same on the destination server anyway.
    """
    if dbname:
        db = Database.objects.get(name=dbname)

        schema = {'tables':{}}

        for tablename in tablenames:
            table = Table.objects.get(db=db, name=tablename)
            schema['tables'][tablename] = []

            for column in Column.objects.filter(table=table):
                schema['tables'][tablename].append((column.name, column.type))

        if destdb:
            schema['database'] = destdb
        else:
            schema['database'] = dbname

        return json.dumps(schema, sort_keys=True)
    
    else:
        schema = {}
        for db in Database.objects.all():
            schema[db.name] = {}
            for table in Table.objects.filter(db=db):
                schema[db.name][table.name] = {}
                for column in Column.objects.filter(table=table):
                    schema[db.name][table.name][column.name] = column.type

        return json.dumps(schema, sort_keys=True)

def json2schema(schema_json, commit = True, dbname = None):
    """
    Creates Database, Table, and Column objects as needed to satisfy the incoming schema.
    If the table is already present, assume we are updating: delete all columns and recreate from the schema.
    Unless commit is false, call the required sql to create the incoming tables in the destination database.
    """

    schema = json.loads(schema_json)

    if dbname is None:
        dbname = schema['database']

    try:
        db = Database.objects.get(name=dbname)
    except Database.DoesNotExist:
        db = Database(name=dbname)
        db.save()

    for (tablename, columns) in schema['tables'].iteritems():
        try:
            table = Table.objects.get(db=db, name=tablename)
            for column in Column.objects.filter(table=table):
                column.delete()
        except Table.DoesNotExist:
            table = Table(db=db, name=tablename)
            table.save()

        for columninfo in columns:
            column = Column(table=table, name=columninfo[0], type=columninfo[1])
            column.save()

        if commit:
            model = ModelGenerator.getModel(dbname, tablename)
            cursor = connections[dbname].cursor()
            for sql in ModelGenerator.getSQL(model):
                cursor.execute(sql)

    return None


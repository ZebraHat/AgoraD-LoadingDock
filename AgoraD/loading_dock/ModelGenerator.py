import types
import sys
from models import Database, Table, Column
from django.db import connections
from django.core.management.color import no_style as style
from django.db import models

# Cache for generated models
# Used as such: modelCache[dbname][tablename] = model
modelCache = {}

# Creates a python module that can create
# modules for databases dynamically.
class ModuleGenerator(types.ModuleType):
    def __getattribute__(self, key):

        # handle those pesky expected attributes
        if key in globals():
            return globals()[key]

        # fun with pretending we still have instance methods
        if key == '__getattribute__':
            return lambda k: ModuleGenerator.__getattribute__(self, k)

        moduleName = __name__ + '.' + str(key)

        # prevent pointless module regeneration
        if moduleName in sys.modules:
            return sys.modules[moduleName]

        # if the requested item doesn't look like an attribute, assume it's a database name
        if not key.startswith('__'):
            # Module that dynamically generates table models
            class DatabaseModule(types.ModuleType):
                def __getattribute__(self, dbmkey):
                    if dbmkey in globals():
                        return globals()[dbmkey]

                    if not dbmkey.startswith('__'):
                        return getModel(key, dbmkey)

                    else:
                        raise AttributeError("'module' object has no attribute '%s'" % dbmkey)

            # Add the newly generated module to the list of modules
            # and to the globals for this module so python doesn't get confused
            module = DatabaseModule(moduleName)
            globals()[key] = module
            sys.modules[moduleName] = module
            return module

        raise AttributeError("'module' object has no attribute '%s'" % key)

# Hold a reference to the current module
# so the garbage collector won't delete globals()
# proud hack don't judge
dont_erase_me_bro = sys.modules[__name__]

# Replace current module with database generator module
sys.modules[__name__] = ModuleGenerator(__name__)

def getSQL(model):
    creation = connections[model.__database__].creation
    return creation.sql_create_model(model, style())[0]

# Create a django model for the specified databse and table
# based on information from database introspection
def getModel(dbname, tablename):
    if dbname in modelCache:
        if tablename in modelCache[dbname]:
            return modelCache[dbname][tablename]

    d = {}

    db = Database.objects.get(name = dbname)
    table = Table.objects.get(name = tablename, db=db)
    columns = Column.objects.filter(table = table)

    d['__fields__'] = []
    for c in columns:
        t = eval(c.type)
        d[c.name] = models.__dict__[t[0]](**t[1])
        d['__fields__'].append(c.name)

    d['__database__'] = dbname

    # Cause the database module to be created if it has not already
    sys.modules[__name__].__getattribute__(dbname)
    d['__module__'] = __name__ + '.' + dbname

    class Meta:
        db_table = tablename
#        managed = False

    d['Meta'] = Meta

    model = type(str(tablename), (models.Model,), d)

    # Store generated model in cache
    db_models = modelCache.get(dbname, {})
    db_models[tablename] = model
    modelCache[dbname] = db_models

    return model



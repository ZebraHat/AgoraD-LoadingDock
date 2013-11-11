class GeneratedModelRouter(object):
  def db_for_read(self, model, **hints):
    return getattr(model, '__database__', None)

  def db_for_write(self, model, **hints):
    return getattr(model, '__database__', None)

  def allow_relation(self, obj1, obj2, **hints):
    if getattr(obj1, '__database__', None) is None:
      return None
    if getattr(obj2, '__database__', None) is None:
      return None

    if obj1.__database__ == obj2.__database__:
      return True
    return None

  def allow_syncdb(self, db, model):
    return db == getattr(model, '__database__', None)



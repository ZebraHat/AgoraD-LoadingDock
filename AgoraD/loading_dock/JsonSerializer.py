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
        clazz = ModelGenerator.getModel(destdb, obj['class'])
        o = clazz()
        for f, v in obj['fields'].iteritems():
            o.__dict__[f] = v

        objs.append(o)

    return objs


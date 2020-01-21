from flask.json import JSONEncoder
from . import serializable


class serializeableJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, serializable.Serializable):
            return obj.serialize()
        return super(serializeableJSONEncoder, self).default(obj)

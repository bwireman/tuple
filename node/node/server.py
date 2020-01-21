from flask import Flask, jsonify
from .api.v0_1 import v0_1

application = Flask(__name__)
versions = dict()
versions["versions"] = dict()


def add_version(blueprint, prefix):
    application.register_blueprint(blueprint, url_prefix=prefix)
    versions["versions"][blueprint.name] = prefix


add_version(v0_1, "/v0-1")


@application.route("/")
def summary():
    return jsonify(versions)


if __name__ == "__main__":
    application.run()

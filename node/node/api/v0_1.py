from flask import jsonify, request, Blueprint
from ..helpers import json_encoder
from .. import node

v0_1 = Blueprint("v0-1", "v0-1", url_prefix="/v0-1")
v0_1.json_encoder = json_encoder.serializeableJSONEncoder

n = node.node("http://node:5000", "v0-1")


@v0_1.route("/")
def summary():
    return jsonify(n)


@v0_1.route("/launch", methods=["POST"])
def launch():
    j = request.get_json()
    containers = n.add_pod(
        pod_image=j["image"],
        pod_tag=j["tag"],
        pod_name=j["name"],
        container_count=j["count"],
    )
    return jsonify(containers)


@v0_1.route("/register", methods=["POST"])
def register():
    j = request.get_json()
    nr = n.register(j["path"])
    return jsonify(nr)

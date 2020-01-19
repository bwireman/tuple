from flask import Flask, jsonify, request
from .helpers import json_encoder
from . import node

app = Flask(__name__)
app.json_encoder = json_encoder.serializeableJSONEncoder

n = node.node("localhost:5000", "v0.1")


@app.route("/")
def summary():
    return jsonify(n)


@app.route("/launch", methods=["POST"])
def launch():
    j = request.get_json()
    containers = n.add_pod(
        pod_image=j["Image"],
        pod_tag=j["Tag"],
        pod_name=j["Name"],
        container_count=j["Count"],
    )
    return jsonify(containers)


@app.route("/register", methods=["POST"])
def register():
    j = request.get_json()
    nr = n.register(j["path"])
    return jsonify(nr)


if __name__ == "__main__":
    app.run()

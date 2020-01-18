from flask import Flask, jsonify, request
from .helpers import json_encoder
from . import node

app = Flask(__name__)
app.json_encoder = json_encoder.serializeableJSONEncoder


n = node.node()
n.add_pod("test", "test", container_count=2)
n.add_pod("test2", "test2", container_count=3)


@app.route("/")
def summary():
    return jsonify(n)


@app.route("/launch", methods=["POST"])
def launch():
    j = request.get_json()
    containers = n.add_pod(
        pod_image=j["image"],
        pod_tag=j["tag"],
        pod_name=j["name"],
        container_count=j["count"],
    )
    return jsonify(containers)


if __name__ == "__main__":
    app.run()

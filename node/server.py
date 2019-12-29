from flask import Flask, jsonify
from .helpers import json_encoder
from . import node

app = Flask(__name__)
app.json_encoder = json_encoder.serializeableJSONEncoder

n = node.node()
n.add_container("test", container_count=3)
n.add_container("test2", container_count=3)


@app.route("/")
def root():
    return jsonify(n)


if __name__ == "__main__":
    app.run()

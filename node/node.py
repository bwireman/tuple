import uuid
import docker
from .helpers import serializable
from .containers import container_wrapper
import requests


class node(serializable.Serializable):
    def __init__(self, node_path, api_version, env=None):
        self.registered = False
        self._uid = uuid.uuid1().hex
        self.pods = dict()
        self.env = env if env else docker.from_env()
        self.pilot_path = None
        self.node_path = node_path
        self.api_version = api_version

    def get_uid(self):
        return self._uid

    def add_pod(
        self,
        pod_image,
        pod_name,
        pod_tag="latest",
        container_count=1,
        restart_on_failure=True,
    ):
        if pod_name in self.pods:
            raise Exception("pod name already in use")

        added = []
        for i in range(container_count):
            cw = container_wrapper.container_wrapper(
                pod_image,
                tag=pod_tag,
                name=pod_name + "-" + str(i),
                restart=restart_on_failure,
            )
            added.append(cw)
            cw.run(self.env)
        self.pods[pod_name] = added

        return self.pods

    def get_pod(self, pod_name):
        return self.pods[pod_name]

    def stop_pod(self, pod_name):
        for cw in self.pods[pod_name]:
            cw.stop()

    def remove_pod(self, pod_name):
        for cw in self.pods[pod_name]:
            cw.remove()

    def kill_pod(self, pod_name):
        for cw in self.pods[pod_name]:
            cw.kill()

    def serialize(self):
        return {
            "uuid": self.get_uid(),
            "pods": {p: [cw.serialize() for cw in v] for p, v in self.pods.items()},
            "registered": self.registered,
            "node_path": self.node_path,
            "api_version": self.api_version,
        }

    def register(self, pilot_path):
        if not self.registered:
            self.registered = True
            self.pilot_path = pilot_path

        nodeRegistry = {
            "node_path": self.node_path,
            "uuid": self.get_uid(),
            "api_version": self.api_version,
        }

        node_path = pilot_path + "/" + self.api_version + "/register"
        print(node_path)
        print(nodeRegistry)
        r = requests.post(node_path, json=nodeRegistry)
        return r.status_code, r.reason

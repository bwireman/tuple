import uuid
import docker
from .helpers import serializable
from .containers import container_wrapper


class node(serializable.Serializable):
    def __init__(self, env=None):
        self._uid = uuid.uuid1().hex
        self.pods = dict()
        self.env = env if env else docker.from_env()

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
            "uid": self._uid,
            "pods": self.pods,
        }

import uuid
import docker
from .helpers import serializable
from .containers import container_wrapper


class node(serializable.Serializable):
    def __init__(self, env=None):
        self._uid = uuid.uuid1().hex
        self.containers = list()
        self.env = env if env else docker.from_env()

    def get_uid(self):
        return self._uid

    def add_container(
        self,
        container_image,
        container_tag="latest",
        container_name=None,
        container_count=1,
    ):
        for _ in range(container_count):
            cw = container_wrapper.container_wrapper(container_image, container_tag)
            self.containers.append(cw)
            cw.run(self.env)

        return self.containers

    def serialize(self):
        return {
            "uid": self._uid,
            "containers": self.containers,
        }

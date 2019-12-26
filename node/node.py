import uuid
import docker
from containers.container_wrapper import container_wrapper


class node:
    def __init__(self, env=None):
        self._uid = uuid.uuid1().hex
        self.container_wrappers = list()
        self.env = env if env else docker.from_env()

    def add_container(
        self,
        container_image,
        container_tag="latest",
        container_name=None,
        container_count=1,
    ):
        for _ in range(container_count):
            cw = container_wrapper(container_name, container_tag)
            self.container_wrappers.append(cw)
            cw.run(self.env)


if __name__ == "__main__":
    n = node()
    n.add_container("test", container_count=3)

from node.containers.container_wrapper import container_wrapper
import docker


def test_basic():
    cw = container_wrapper("ubuntu", restart=False)
    cw.run(docker.from_env())
    assert cw.get_status() == "running"
    cw.kill()
    cw.get_status() == "stopped"


def test_basic_restart_true():
    cw = container_wrapper("ubuntu", restart=True)
    cw.run(docker.from_env())
    assert cw.get_status() == "running"
    cw.kill()
    cw.get_status() == "stopped"

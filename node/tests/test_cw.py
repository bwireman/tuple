from node.containers.container_wrapper import container_wrapper
import docker


def test_basic():
    cw = container_wrapper("test", restart=False)
    cw.run(docker.from_env(), heartbeatRhythm=1)
    assert cw.get_status() == "running"
    cw.kill()
    cw.get_status() == "stopped"


def test_basic_restart_true():
    cw = container_wrapper("test", restart=True)
    cw.run(docker.from_env(), heartbeatRhythm=1)
    assert cw.get_status() == "running"
    cw.kill()
    cw.get_status() == "stopped"

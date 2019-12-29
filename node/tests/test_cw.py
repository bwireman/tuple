from ..containers import container_wrapper
import docker

def test_basic():
    cw = container_wrapper.container_wrapper("test", restart=False)
    cw.run(docker.from_env(), heartbeatRhythm=1)
    assert cw.get_status() == "running"
    cw.kill()
    assert cw.get_status() == "exited"


def test_basic_restart_true():
    cw = container_wrapper.container_wrapper("test", restart=True)
    cw.run(docker.from_env(), heartbeatRhythm=1)
    assert cw.get_status() == "running"
    cw.kill()
    assert cw.get_status() == "exited"


def test_basic_stop():
    cw = container_wrapper.container_wrapper("test", restart=True)
    cw.run(docker.from_env(), heartbeatRhythm=1)
    assert cw.get_status() == "running"
    cw.stop()
    assert cw.get_status() == "exited"


def test_serialize():
    cw = container_wrapper.container_wrapper("test", name="test-serialize", restart=True)
    assert cw.serialize() == {
        "image": "test",
        "tag": "latest",
        "name": "test-serialize",
        "status": "not started",
        "restart_on_failure": True
    }
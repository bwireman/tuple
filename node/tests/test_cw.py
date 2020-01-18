from ..containers import container_wrapper
import docker


def test_basic():
    cw = container_wrapper.container_wrapper("test", restart=False, name="cw-basic")
    cw.run(docker.from_env(), heartbeatRhythm=1)
    assert cw.get_status() == "running"
    cw.kill()
    assert cw.get_status() == "removed"


def test_remove():
    cw = container_wrapper.container_wrapper("test", restart=False, name="cw-remove")
    cw.run(docker.from_env(), heartbeatRhythm=1)
    assert cw.get_status() == "running"
    cw.stop()
    assert cw.get_status() == "stopped"
    cw.remove()
    assert cw.get_status() == "removed"


def test_restart():
    cw = container_wrapper.container_wrapper("test", restart=True, name="cw-restart")
    cw.run(docker.from_env(), heartbeatRhythm=1)
    assert cw.get_status() == "running"
    cw.container.stop()
    assert cw.get_status() == "exited"
    cw.stop()
    cw.remove()


def test_stop():
    cw = container_wrapper.container_wrapper("test", restart=True, name="cw-stop")
    cw.run(docker.from_env(), heartbeatRhythm=1)
    assert cw.get_status() == "running"
    cw.stop()
    assert cw.get_status() == "stopped"
    cw.remove()


def test_serialize():
    cw = container_wrapper.container_wrapper(
        "test", name="test-serialize", restart=True
    )
    assert cw.serialize() == {
        "image": "test",
        "tag": "latest",
        "name": "test-serialize",
        "status": "not started",
        "restart_on_failure": True,
    }

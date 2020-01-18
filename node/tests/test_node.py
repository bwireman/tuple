from .. import node


def test_constructor():
    n = node.node()
    name = "node-test-constructor"
    n.add_pod("test", name, container_count=2)
    assert n.get_pod(name)[0].get_status() == "running"
    assert n.get_pod(name)[1].get_status() == "running"
    n.get_pod(name)[0].kill()
    assert n.get_pod(name)[0].get_status() == "removed"
    assert n.get_pod(name)[1].get_status() == "running"
    n.get_pod(name)[1].kill()
    assert n.get_pod(name)[1].get_status() == "removed"
    n.kill_pod(name)


def test_serialize():
    n = node.node()
    name = "node-test-serialize"
    n.add_pod("test", name, container_count=2)
    n.serialize()["pods"] = {
        name: [
            {
                "image": "test",
                "name": "node-test-serialize-0",
                "restart_on_failure": True,
                "status": "running",
                "tag": "latest",
            },
            {
                "image": "test",
                "name": "node-test-serialize-1",
                "restart_on_failure": True,
                "status": "running",
                "tag": "latest",
            },
        ]
    }
    n.kill_pod(name)

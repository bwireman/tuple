from .. import node

def test_constructor():
    n = node.node()
    containers = n.add_container("test", container_count=2)
    assert containers[0].get_status() == "running"
    assert containers[1].get_status() == "running"
    containers[1].kill()
    assert containers[1].get_status() == "exited"
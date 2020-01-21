import requests


def post(path, data):
    resp = requests.post(path, json=data)

    try:
        out = resp.json()
    except Exception:
        out = resp.text

    return out

def get(path):
    return requests.get(path).json()


def test_node_status():
    node_status = get("http://node:5000")
    assert node_status == {"versions": {"v0-1": "/v0-1"}}


def test_pilot_status():
    pilot_staus = get("http://pilot:5001/")
    assert pilot_staus == {"versions": {"v0-1": "/v0-1"}}


def test_launch():
    # get uuids
    pilot_uuid = get("http://pilot:5001/v0-1/")["uuid"]
    node_uuid = get("http://node:5000/v0-1/")["uuid"]
    
    # register node
    registered = post("http://node:5000/v0-1/register", {"path": "http://pilot:5001"})
    assert registered == [200, "OK"]
    
    # test that node is registered
    pilot_status = get("http://pilot:5001/v0-1/")
    expected_registered = {
        "uuid": pilot_uuid,
        "nodes": [
            {"uuid": node_uuid, "node_path": "http://node:5000", "api_version": "v0-1",}
        ],
    }
    assert pilot_status == expected_registered 

    # launch test pod
    launched = post("http://pilot:5001/v0-1/launch", { "image":"ubuntu", "tag":"latest", "name":"TEST", "count":2 })
    assert launched == "200 OK"

    node_status_launched = get("http://node:5000/v0-1/")
    node_status_launched_expected = {
        "api_version": "v0-1",
        "node_path": "http://node:5000",
        "pods": {
            "TEST": [
                {
                    "image": "ubuntu",
                    "name": "TEST-0",
                    "restart_on_failure": True,
                    "status": "running",
                    "tag": "latest",
                },
                {
                    "image": "ubuntu",
                    "name": "TEST-1",
                    "restart_on_failure": True,
                    "status": "running",
                    "tag": "latest",
                },
            ]
        },
        "registered": True,
        "uuid": node_uuid,
    }
    assert node_status_launched == node_status_launched
# tests/test_layers.py
import json

def test_layers_crud(client):
    # must be logged in first
    client.post("/login", data={"username": "alice", "password": "secret123"})

    # 1) create a layer
    payload = {
        "site": "SiteA",
        "sector": "Sector1",
        "square": "A1",
        "context": "ContextX",
        "layer": "L1",
        "stratum": "S1",
        "level": 5,
        "structure": "struc"
    }
    resp = client.post("/layers/add", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data
    layer_id = data["id"]

    # 2) list (with pagination metadata)
    resp = client.get("/layers?page=1")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body["items"], list)
    assert body["metadata"]["page"] == 1

    # 3) update
    update_payload = payload.copy()
    update_payload["level"] = 10
    resp = client.put(f"/layers/{layer_id}", json=update_payload)
    assert resp.status_code == 200
    assert resp.json()["level"] == 10

    # 4) delete
    resp = client.delete(f"/layers/{layer_id}")
    assert resp.status_code == 204

    # 5) confirm gone
    resp = client.get(f"/layers/{layer_id}")
    assert resp.status_code == 404

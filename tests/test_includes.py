# tests/test_includes.py
def make_include_payload():
    return {
        "layer_id": 1,
        "type": "Ceramic",
        "count": 42
    }

def test_includes_crud(client, db_session):
    # create a layer in the DB directly
    from src.models import Tbllayer
    layer = Tbllayer(site="X", sector="Y", square="Z", context="C", layer="L", stratum="S", level=1, structure="Struc")
    db_session.add(layer)
    db_session.commit()

    client.post("/login", data={"username": "alice", "password": "secret123"})
    # Create
    resp = client.post("/layer_includes/add", json=make_include_payload())
    assert resp.status_code == 201
    inc_id = resp.json()["id"]
    # Read/List
    resp = client.get("/layer_includes?page=1")
    assert resp.status_code == 200
    # Update
    resp = client.put(f"/layer_includes/{inc_id}", json={"count": 100})
    assert resp.json()["count"] == 100
    # Delete
    resp = client.delete(f"/layer_includes/{inc_id}")
    assert resp.status_code == 204

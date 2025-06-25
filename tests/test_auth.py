# tests/test_auth.py
import pytest

def test_register_login_logout(client):
    # 1) register a new user
    resp = client.post(
        "/register",
        data={
            "username": "alice",
            "email": "alice@example.com",
            "password": "secret123",
            "password2": "secret123"
        },
        follow_redirects=False
    )
    # expecting a redirect to login or to index
    assert resp.status_code in (302, 303)

    # 2) login
    resp = client.post(
        "/login",
        data={"username": "alice", "password": "secret123"},
        allow_redirects=False
    )
    assert resp.status_code in (302, 303)
    # should set a session cookie
    assert "session" in resp.cookies or "Authorization" in resp.headers.get("set-cookie", "")

    # 3) access a protected page
    resp = client.get("/", follow_redirects=True)
    assert resp.status_code == 200
    assert "Logout" in resp.text

    # 4) logout
    resp = client.get("/logout", follow_redirects=True)
    assert resp.status_code == 200
    # after logout, index should redirect to login
    resp = client.get("/", allow_redirects=False)
    assert resp.status_code in (302, 303)

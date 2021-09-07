from tests.defaults import DEFAULT_REGISTER_PARAMS


def test_register(client, db):
    resp = client.post("/users/register/", DEFAULT_REGISTER_PARAMS)
    assert "access" in resp.json()
    assert "refresh" in resp.json()


def test_login(client, user):
    resp = client.post(
        "/users/login/", {"email": user.email, "password": "member_password"}
    )
    assert "access" in resp.json()
    assert "refresh" in resp.json()


def test_me(authenticated_client, user):
    resp = authenticated_client.get("/users/me/")
    assert user.username in resp.json()["username"]
    assert user.email in resp.json()["email"]

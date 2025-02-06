from src.enums import AccountType


def test_request_without_auth(client):
    result = client.get("/applications/")
    assert result.status_code == 401
    assert "Not authenticated" in result.json().get("detail")


def test_login_with_unexist_user(client):
    data = {
        "username": "wrongUsername",
        "password": "testpassword"
    }
    result = client.post("/auth/login/", data=data)

    assert result.status_code == 401
    assert "Incorrect username of password" in result.json().get("detail")
    

def test_login_with_exist_user(client, user):
    data = {
        "username": user.username,
        "password": "testpassword"
    }
    result = client.post("/auth/login/", data=data)

    assert result.status_code == 200
    assert result.json().get("access_token")
    assert result.json().get("refresh_token")


def test_refresh_token(client_with_auth, refresh_token):
    result = client_with_auth.post("/auth/refresh/")
    assert result.status_code == 200
    assert result.json().get("refresh_token")
    



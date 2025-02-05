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
    

def test_create_user(client):
    data = {
        "email": "testemail@gmail.com",
        "username": "test_username",
        "password": "testpassword",
        "account_type": AccountType.tester.value
    }
    result = client.post("/users/", json=data)
    assert result.status_code == 201
    assert "test_username" in result.json().get("username")
    assert "testemail@gmail.com" in result.json().get("email")

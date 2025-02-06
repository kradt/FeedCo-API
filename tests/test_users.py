from src.enums import AccountType
from src.users.models import User
from src.applications.models import Application


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


def test_get_all_users(client_with_auth):
    response = client_with_auth.get("/users/", params={"search_pattern": ""})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user(client_with_auth, user):
    response = client_with_auth.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json()["email"] == user.email


def test_get_me(client_with_auth, user):
    response = client_with_auth.get("/users/me/")
    assert response.status_code == 200
    assert response.json()["email"] == user.email


def test_get_current_user_applications(client_with_auth, user, application):
    response = client_with_auth.get("/users/me/applications/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_specific_user_applications(client_with_auth, user, application):
    response = client_with_auth.get(f"/users/{user.id}/applications/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_user(client_with_auth, user):
    update_data = {"username": "updateduser"}
    response = client_with_auth.patch("/users/me/", json=update_data)
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"


def test_delete_user(client_with_auth, user):
    response = client_with_auth.delete("/users/me/")
    assert response.status_code == 204
    response = client_with_auth.get(f"/users/{user.id}")
    # because of user was logged in
    assert response.status_code == 401

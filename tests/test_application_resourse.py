from src.enums import RatingGrade


def test_get_applications(client_with_auth):
    response = client_with_auth.get("/applications/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_application(client_with_auth, application):
    response = client_with_auth.get(f"/applications/{application.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test App"


def test_create_application(client_with_auth):
    data = {"name": "New App", "description": "stringstringstringstringstringstringstringstringklklkklklstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringstringst"}
    response = client_with_auth.post("/applications/", json=data)
    assert response.status_code == 201
    assert response.json()["name"] == "New App"


def test_create_rating(client_with_auth, application, user):
    rating_data = {"grade": RatingGrade.grade_5.value, "user_id": user.id}
    response = client_with_auth.post(f"/applications/{application.id}/rating", json=rating_data)
    assert response.status_code == 201
    assert response.json()["grade"] == RatingGrade.grade_5.value


def test_get_application_ratings(client_with_auth, application):
    response = client_with_auth.get(f"/applications/{application.id}/rating")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_application(client_with_auth, application):
    update_data = {"name": "Updated App"}
    response = client_with_auth.patch(f"/applications/{application.id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated App"


def test_delete_application(client_with_auth, application):
    response = client_with_auth.delete(f"/applications/{application.id}")
    assert response.status_code == 204
    response = client_with_auth.get(f"/applications/{application.id}")
    assert response.status_code == 404

from src.reviews.models import Review, ReviewVotes
from src.comments.models import Comment
from src.users.models import User


def test_get_review(client_with_auth, review, user):
    response = client_with_auth.get(f"/reviews/{review.id}")
    assert response.status_code == 200
    assert response.json()["body"] == review.body


def test_update_review(client_with_auth, review, user):
    update_data = {"body": "Updated review content"}
    response = client_with_auth.patch(f"/reviews/{review.id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["body"] == "Updated review content"


def test_get_review_comments(client_with_auth, review, user):
    response = client_with_auth.get(f"/reviews/{review.id}/comments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_comment(client_with_auth, review, user):
    comment_data = {"text": "This is a test comment", "user_id": user.id}
    response = client_with_auth.post(f"/reviews/{review.id}/comments", json=comment_data)
    assert response.status_code == 201
    assert response.json()["text"] == "This is a test comment"


def test_get_comment(client_with_auth, comment, user):
    response = client_with_auth.get(f"/comments/{comment.id}/")
    assert response.status_code == 200
    assert response.json()["text"] == comment.text


def test_create_vote_on_review(session, client_with_auth, review, user):
    vote_data = {"user_id": user.id, "vote_type": True}
    response = client_with_auth.post(f"/reviews/{review.id}/votes", json=vote_data)
    assert response.status_code == 201

    # Verify that the vote is created
    vote = session.query(ReviewVotes).filter_by(review_id=review.id, user_id=user.id).first()
    assert vote is not None


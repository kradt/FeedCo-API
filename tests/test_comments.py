from src.enums import RatingGrade
from src.comments.models import Comment, CommentVotes
from src.users.models import User


def test_get_comment(client_with_auth, comment, user):
    response = client_with_auth.get(f"/comments/{comment.id}")
    assert response.status_code == 200
    assert response.json()["text"] == comment.text


def test_update_comment(client_with_auth, comment, user):
    update_data = {"text": "Updated comment content"}
    response = client_with_auth.patch(f"/comments/{comment.id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["text"] == "Updated comment content"


def test_create_vote_on_comment(session, client_with_auth, comment, user):
    vote_data = {"user_id": user.id, "vote_type": True, "comment_id": comment.id}
    response = client_with_auth.post(f"/comments/{comment.id}/votes", json=vote_data)
    assert response.status_code == 201

    vote = session.query(CommentVotes).filter_by(comment_id=comment.id, user_id=user.id).first()
    assert vote is not None


def test_delete_comment(client_with_auth, comment, user):
    response = client_with_auth.delete(f"/comments/{comment.id}")
    assert response.status_code == 204

    response = client_with_auth.get(f"/comments/{comment.id}")
    assert response.status_code == 404

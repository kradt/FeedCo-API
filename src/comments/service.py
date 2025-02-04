from sqlalchemy.orm import Session

from src.comments import models
from src.comments.schemas import CommentBase, CommentCreate, VoteCreate


def create(db: Session, comment_data: CommentCreate, review_id):
    comment = models.Comment(text=comment_data.text, review_id=review_id, user_id=comment_data.user_id)
    db.add(comment)
    db.commit()
    return comment


def get(db: Session, comment_id: int):
    return db.query(models.Comment).filter_by(id=comment_id).first()


def update(db: Session, comment_data: CommentBase, comment_id: int):
    comment = get(db, comment_id)
    if comment_data.text:
        comment.text = comment_data.text
    db.add(comment)
    db.commit()


def delete(db: Session, comment_id: int):
    comment = get(db, comment_id)
    comment.deleted = True
    db.add(comment)
    db.commit()


def vote_exist(db: Session, votes_data: VoteCreate, comment_id: int) -> bool:
    vote = db.query(models.CommentVotes).filter_by(user_id=votes_data.user_id, comment_id=comment_id).first()
    return vote


def vote(db: Session, votes_data: VoteCreate, comment_id: int):
    vote = vote_exist(db, votes_data, comment_id)
    if vote:
        vote.vote_type = votes_data.vote_type
    else:
        vote = models.CommentVotes(vote_type=votes_data.vote_type, comment_id=comment_id, user_id=votes_data.user_id)
    db.add(vote)
    db.commit()
    return vote


def unvote(db: Session, votes_data: VoteCreate, comment_id: int):
    vote = vote_exist(db, votes_data, comment_id)
    db.delete(vote)
    db.commit()

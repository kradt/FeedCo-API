from src.database.core import SessionLocal
from src.reviews import models
from src.reviews.schemas import ReviewBase
from src.comments.schemas import VoteCreate

from sqlalchemy.orm import Session


def get(db: Session, review_id: int):
    return db.query(models.Review).filter_by(id=review_id).first()


def update(db: Session, review_data: ReviewBase, review_id: int):
    review = get(db, review_id)
    if review_data.title:
        review.title = review_data.title
    if review_data.body:
        review.body = review_data.body
    db.add(review)
    db.commit()
    return review


def vote_exist(db: Session, votes_data: VoteCreate, review_id: int) -> bool:
    vote = db.query(models.ReviewVotes).filter_by(user_id=votes_data.user_id, review_id=review_id).first()
    return vote


def vote(db: Session, votes_data: VoteCreate, review_id: int):
    vote = vote_exist(db, votes_data, review_id)
    if vote:
        vote.vote_type = votes_data.vote_type
    else:
        vote = models.ReviewVotes(vote_type=votes_data.vote_type, review_id=review_id, user_id=votes_data.user_id)
    db.add(vote)
    db.commit()
    return vote


def unvote(db: Session, votes_data: VoteCreate, review_id: int):
    vote = vote_exist(db, votes_data, review_id)
    db.delete(vote)
    db.commit()

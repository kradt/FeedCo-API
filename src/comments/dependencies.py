from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Path, Body
from src.comments.schemas import CommentCreate, VoteCreate
from src.dependencies import get_db
from src.reviews.dependencies import get_review_by_id
from src.users import service as user_service
from src.comments import service
from src.reviews import models


def create_comment(
        db: Annotated[Session, Depends(get_db)],
        review: Annotated[models.Review, Depends(get_review_by_id)],
        comment_data: Annotated[CommentCreate, Body()], 
        review_id: Annotated[int, Path()]):
    user = user_service.get(db, comment_data.user_id)
    if not user:
        raise HTTPException(404, detail=f"User with id {comment_data.user_id} is not found")
    return service.create(db, comment_data, review_id)


def get_comment_by_id(
        db: Annotated[Session, Depends(get_db)],
        comment_id: Annotated[int, Path()]):
    comment = service.get(db, comment_id)
    if not comment:
        raise HTTPException(404, detail=f"There is no comment with id {comment_id}")
    return comment


def vote_comment(
        db: Annotated[Session, Depends(get_db)],
        comment: Annotated[models.Comment, Depends(get_comment_by_id)],
        votes_data: Annotated[VoteCreate, Body()]):
    user = user_service.get(db, votes_data.user_id)
    if not user:
        raise HTTPException(404, detail=f"User with id {votes_data.user_id} is not found")
    return service.vote(db, votes_data, comment.id)
    

def unvote_comment(
        db: Annotated[Session, Depends(get_db)],
        comment: Annotated[models.Comment, Depends(get_comment_by_id)],
        votes_data: Annotated[VoteCreate, Body()]):
    user = user_service.get(db, votes_data.user_id)
    if not user:
        raise HTTPException(404, detail=f"User with id {votes_data.user_id} is not found")
    return service.unvote(db, votes_data, comment.id)
    
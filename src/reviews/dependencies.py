
from typing import Annotated

from fastapi import Depends, Path, HTTPException, Body
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.reviews import service, models
from src.comments.schemas import VoteCreate
from src.users import service as user_service


async def get_review_by_id(db: Annotated[Session, Depends(get_db)], review_id: Annotated[int, Path()]):
    review = service.get(db, review_id)
    if not review:
        raise HTTPException(404, detail=f"There is no review with id {review_id}")
    return review


async def vote_review(
        db: Annotated[Session, Depends(get_db)],
        review: Annotated[models.Review, Depends(get_review_by_id)],
        votes_data: Annotated[VoteCreate, Body()]):
    user = user_service.get(db, votes_data.user_id)
    if not user:
        raise HTTPException(404, detail=f"User with id {votes_data.user_id} is not found")
    return service.vote(db, votes_data, review.id)
    

async def unvote_review(
        db: Annotated[Session, Depends(get_db)],
        comment: Annotated[models.Comment, Depends(get_review_by_id)],
        votes_data: Annotated[VoteCreate, Body()]):
    user = user_service.get(db, votes_data.user_id)
    if not user:
        raise HTTPException(404, detail=f"User with id {votes_data.user_id} is not found")
    return service.unvote(db, votes_data, comment.id)

from typing import Annotated

from fastapi import APIRouter, Depends, Security, Body

from src.comments.schemas import CommentFull
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.reviews import models, service
from src.reviews.dependencies import get_review_by_id, vote_review, unvote_review
from src.users import models as user_models
from src.auth.dependencies import get_current_user
from src.reviews.schemas import ReviewFull, ReviewBase, ReviewUpdate
from src.comments.schemas import VoteCreate
from src.comments.dependencies import create_comment, get_comment_by_id

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/{review_id}", response_model=ReviewFull)
async def get_review_by_id(
        review: Annotated[models.Review, Depends(get_review_by_id)],
        current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])]):
    return review


@router.patch("/{review_id}", response_model=ReviewFull)
async def update_review(
        db: Annotated[Session, Depends(get_db)],
        review: Annotated[models.Review, Depends(get_review_by_id)],
        review_data: Annotated[ReviewUpdate, Body()],
        current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])]):
    return service.update(db, review_data, review.id)


@router.get("/{review_id}/comments", response_model=list[CommentFull])
async def get_review_comments(
        db: Annotated[Session, Depends(get_db)],
        review: Annotated[models.Review, Depends(get_review_by_id)],
        current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])]):
    return review.comments


@router.post("/{review_id}/comments", response_model=CommentFull, status_code=201)
async def create_comment(
        comment: Annotated[models.Comment, Depends(create_comment)],
        current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])]):
    return comment


@router.get("/{comment_id}/", response_model=CommentFull)
async def get_comment_by_id(
    comment: Annotated[CommentFull, Depends(get_comment_by_id)],
    current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])]):
    return comment


@router.post("/{review_id}/votes", response_model=VoteCreate, status_code=201)
async def create_vote_on_review(
        vote: Annotated[models.ReviewVotes, Depends(vote_review)],
        current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])]):
    return vote


@router.delete("/{review_id}/votes", status_code=204)
async def delete_vote_on_review(
        vote: Annotated[None, Depends(unvote_review)],
        current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])]):
    return None

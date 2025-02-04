from typing import Annotated

from fastapi import APIRouter, Depends, Security, Body

from src.comments.schemas import CommentBase, CommentFull, VoteCreate
from sqlalchemy.orm import Session
from src.dependencies import get_db
from src.comments import service, models
from src.users import models as user_models
from src.auth.dependencies import get_current_user
from src.comments.dependencies import get_comment_by_id, unvote_comment, vote_comment

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/{comment_id}", response_model=CommentFull)
async def get_comment_by_id(
        comment: Annotated[models.Comment, Depends(get_comment_by_id)],
        current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])]):
    return comment


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(
        db: Annotated[Session, Depends(get_db)],
        comment: Annotated[models.Comment, Depends(get_comment_by_id)],
        current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])]):
    service.delete(db, comment.id)


@router.patch("/{comment_id}", response_model=CommentFull)
async def update_comment(
        db: Annotated[Session, Depends(get_db)],
        comment: Annotated[models.Comment, Depends(get_comment_by_id)],
        comment_data: Annotated[CommentBase, Body()],
        current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])]):
    return service.update(db, comment_data, comment.id)


@router.post("/{comment_id}/votes", response_model=VoteCreate)
async def create_vote_on_comment(
        vote: Annotated[models.CommentVotes, Depends(vote_comment)],
        current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])]):
    return vote


@router.delete("/{comment_id}/votes", status_code=204)
async def delete_vote_on_comment(
        vote: Annotated[None, Depends(unvote_comment)],
        current_user: Annotated[user_models.User, Security(get_current_user, scopes=["applications"])]):
    return None

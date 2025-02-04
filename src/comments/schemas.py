from pydantic import BaseModel


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    user_id: int


class CommentFull(CommentBase):
    id: int
    votes_positive: int
    votes_negative: int


class VoteCreate(BaseModel):
    vote_type: bool
    user_id: int


class CommentVoteFull(BaseModel):
    comment_id: int
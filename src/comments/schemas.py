from pydantic import BaseModel


class CommentBase(BaseModel):
    text: str


class CommentFull(CommentBase):
    votes_positive: int
    votes_negative: int

from sqlmodel import SQLModel, Field


class GroupUserLink(SQLModel, table=True):
    __tablename__ = 'groupuserlink'
    user_id: int = Field(
        primary_key=True, foreign_key='user.id', default=None
    )
    group_id: int = Field(
        primary_key=True, foreign_key='group.id', default=None
    )

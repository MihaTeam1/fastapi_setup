import uuid as uuid_pkg
from typing import Optional
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlmodel import Field, SQLModel


class IDModelBase(SQLModel):
    id: Optional[int] = Field(
                default=None,
                primary_key=True,
                index=True,
                nullable=False,
            )
    updated_at: Optional[datetime] = Field(sa_column=Column(
                DateTime(timezone=True),
                nullable=False,
                server_default=func.now(),
                onupdate=func.now(),
            ))
    created_at: Optional[datetime] = Field(sa_column=Column(
                DateTime(timezone=True),
                nullable=False,
                server_default=func.now(),
            ))


class UUIDModelBase(IDModelBase):
    id: uuid_pkg.UUID = Field(sa_column=Column(
                UUID(as_uuid=True),
                default=uuid_pkg.uuid4,
                server_default=text("gen_random_uuid()"),
                primary_key=True,
                index=True,
                nullable=False,
                unique=True,
            ))
        
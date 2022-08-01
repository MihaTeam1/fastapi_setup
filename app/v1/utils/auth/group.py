from sqlalchemy.ext.asyncio import AsyncSession

from schemas.group import GroupCreate, GroupModel, GroupRead, AddUserToGroup
from models.links import GroupUserLink


async def create_group(group: GroupCreate, session: AsyncSession) -> GroupRead:
    group = GroupModel(
        name=group.name
    )
    session.add(group)
    await session.commit()
    await session.refresh(group)
    return group


async def add_user_to_group(group: AddUserToGroup, session: AsyncSession):
    link = GroupUserLink(
        user_id=group.user_id,
        group_id=group.group_id,
    )
    session.add(link)
    await session.commit()
    await session.refresh(link)
    return link
from models.permission import PermissionBase, Base, PermissionModel


class PermissionRead(Base, PermissionBase):
    pass


class PermissionCreate(PermissionBase):
    pass


class PermissionReadWithUsers(PermissionRead):
    from .user import UserRead
    user: UserRead


from fastapi import APIRouter

from .endpoints import user, token, permission, group


router = APIRouter(prefix='/v1')
router.include_router(router=user.router)
router.include_router(router=token.router)
router.include_router(router=permission.router)
router.include_router(router=group.router)
from fastapi import APIRouter

from .endpoints import user

router = APIRouter(prefix='/v1')
router.include_router(router=user.router)

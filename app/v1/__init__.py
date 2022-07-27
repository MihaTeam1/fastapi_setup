from fastapi import APIRouter

from .endpoints import auth

router = APIRouter(prefix='/v1')
router.include_router(router=auth.router)

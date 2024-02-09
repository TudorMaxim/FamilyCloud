import config
from fastapi import APIRouter

router = APIRouter(
    prefix='/users',
    tags=[]
)

@router.get('/')
async def all_users():
    return [config.DEFAULT_USER]

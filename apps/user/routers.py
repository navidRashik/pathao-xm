from fastapi import APIRouter
from apps.user.views.users import post_user
user_router = APIRouter(
    prefix="/users",
    # tags=['users'],
    responses={404: {"description": "Not found"}},
)


user_router.add_api_route('/', post_user, methods=['POST'], status_code=201)

routers = [
    user_router,
]

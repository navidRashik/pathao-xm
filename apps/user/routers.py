from fastapi import APIRouter
from apps.user.views.users import post_user, get_user, post_tags, filter_by_tags
user_router = APIRouter(
    prefix="/users",
    # tags=['users'],
    responses={404: {"description": "Not found"}},
)


user_router.add_api_route('/', post_user, methods=['POST'], status_code=201)
user_router.add_api_route('/{id}', get_user, methods=['GET'])
user_router.add_api_route('/{id}/tags', post_tags,
                          methods=['POST'], status_code=201)
user_router.add_api_route('/', filter_by_tags, methods=['GET'])

routers = [
    user_router,
]


# this should be a folder
from apps.items.views.items import read_items, read_item, update_item
from fastapi import HTTPException
from fastapi import APIRouter, Depends
# from chat.common.dependencies import get_token_header
from common.dependencies import get_token_header


item_router = APIRouter(

    prefix="/items",

    tags=["items"],

    dependencies=[Depends(get_token_header)],

    responses={404: {"description": "Not found"}},

)
item_router.add_api_route('/', read_items, methods=['GET'])
item_router.add_api_route('/{item_id}', read_item, methods=['GET'])
item_router.add_api_route(
    "/{item_id}", endpoint=update_item, methods=['PUT'],
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)

routers = [
    item_router,
]

# this should be a folder
from fastapi import HTTPException


async def post_user(firstName: str, lastName: str, password: str):
    
    return {
        "id": 2
    }

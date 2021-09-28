# this should be a folder
from apps.user.validators import UserIn
from fastapi import HTTPException
from main import users_table

async def post_user(user:UserIn):
    query = users_table.insert().values(firstName=user.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}
    return {
        "id": 2
    }

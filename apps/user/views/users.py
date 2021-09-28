# this should be a folder
from apps.user.validators import UserIn
from fastapi import HTTPException
from main import users_table
import jwt
from main import secret_key, secret_algorithm, database


async def post_user(user: UserIn):
    hash_password = jwt.encode(
        {'password': user.password}, secret_key, algorithm=secret_algorithm)
    query = users_table.insert().values(
        first_name=user.first_name, last_name=user.last_name, hash_password=hash_password)
    last_record_id = await database.execute(query)
    return {"id": last_record_id}

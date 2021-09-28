# this should be a folder
from sqlalchemy.sql import operators
from datetime import datetime, timedelta
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


async def get_user(id: int):
    query = users_table.select().where(users_table.c.id == id)
    data = await database.fetch_one(query)

    # values(
    #     first_name=user.first_name, last_name=user.last_name, hash_password=hash_password)
    first_name = data[1]
    last_name = data[2]
    return {
        'id': data[0],
        'name': f"{first_name} {last_name}"
    }


async def post_tags(id: int, tags: list, expiry: int):
    q = users_table.select().where(users_table.c.id == id)
    data = await database.fetch_one(q)
    time_stamp = data[5] if data[5] else datetime.now()
    time_stamp += timedelta(milliseconds=expiry)

    query = users_table.update().where(users_table.c.id == id).values(
        tags=tags, tags_expire_at=time_stamp)
    await database.execute(query)
    return {}


async def filter_by_tags(tags: str):
    tag_list = tags.split(',')
    q = users_table.select().where(
        users_table.c.tags.any(tag_list, operator=operators.in_op))
    data = await database.fetch_all(q)

    # time_stamp = data[5] if data[5] else datetime.now()
    # time_stamp += timedelta(milliseconds=expiry)

    # query = users_table.update().where(users_table.c.id == id).values(
    #     tags=tags, tags_expire_at=time_stamp)
    # await database.execute(query)
    return {"users": data}

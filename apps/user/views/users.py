# this should be a folder
from datetime import datetime, timedelta
from typing import List, Optional

import jwt
from apps.user.validators import UserIn
from fastapi import HTTPException, Query
from main import database, secret_algorithm, secret_key, users_table
from sqlalchemy.sql import operators


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
    if not data:
        raise HTTPException(
            status_code=404, detail="Not Found"
        )
    first_name = data[1]
    last_name = data[2]

    return {
        'id': data[0],
        'name': f"{first_name} {last_name}"
    }


async def post_tags(id: int, tags: list, expiry: int):
    q = users_table.select().where(users_table.c.id == id)
    data = await database.fetch_one(q)
    time_stamp = datetime.now() + timedelta(milliseconds=expiry)

    query = users_table.update().where(users_table.c.id == id).values(
        tags=tags, tags_expire_at=time_stamp)
    await database.execute(query)
    return {}


async def filter_by_tags(tags: Optional[List[str]] = Query(None)):

    q = users_table.select().where(
        users_table.c.tags.overlap(tags), users_table.c.tags_expire_at > datetime.now())

    data = await database.fetch_all(q)
    users = list()

    if not data:
        raise HTTPException(
            status_code=404, detail="Not Found"
        )
    for usr in data:
        first_name = usr[1]
        last_name = usr[2]

        users.append({
            'id': usr[0],
            'name': f"{first_name} {last_name}",
            'tags': usr.get('tags'),
        })
    return {"users": users}

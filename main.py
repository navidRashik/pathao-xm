from common.dependencies import get_token_header
from fastapi import APIRouter, Depends
from fastapi import APIRouter
from fastapi import Depends, FastAPI
import glob
from common.dependencies import get_query_token, get_token_header
# from .internal import admin
# from apps import items, user

import importlib.util
import logging

app = FastAPI(dependencies=[Depends(get_query_token)])

@app.get("/")
async def root():
    return {"message": "Health is Ok"}


@app.on_event("startup")
async def handle_startup():
    router_list = list()
    for file_name in glob.iglob('./**/routers.py', recursive=True):
        print('-----------------loop')
        print(file_name)
        spec = importlib.util.spec_from_file_location('routers', file_name)
        each_app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(each_app)
        router_list += each_app.routers
        print(router_list)

    for rt in router_list:
        print(rt)
        app.include_router(rt)

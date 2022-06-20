from typing import Any

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError

# from fastapi.encoders import jsonable_encoder

from api.crud import ItemDAL
from db import Base, async_session, engine
from api.models import ItemDB, ItemSchema

from api.lib import update_item_data


class DefaultResponse(JSONResponse):
    def render(self, content: Any) -> bytes:

        return super().render(
            {
                "api_version": "0.1",
                "ok": True if self.status_code in [200, 201] else False,
                "data": content,
            }
        )


app = FastAPI(default_response_class=DefaultResponse)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    error_list = []
    for error in exc.errors():
        field = error.get("loc")[-1]
        error_list.append(
            {
                "field": field,
                "msg_error": f'{error.get("msg")} ({error.get("type")})',
                "field_original": exc.body.get(field),
            }
        )

    return DefaultResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={  # for structures  --  jsonable_encoder()
            "error": [
                f'Field    \
{i["field"]}   with content    \
{i["field_original"]}   \
{i["msg_error"]}'
                for i in error_list
            ]
        },
    )


@app.post(
    "/save_item",
    status_code=201,
)
async def save_item(payload: ItemSchema):
    async with async_session() as session:
        async with session.begin():
            item_dal = ItemDAL(session)
            item = await item_dal.save_item(payload)

            response_obj: ItemDB = {
            }
            return response_obj

@app.get("/get_items")
async def get_all_items():
    """
    return all data structures"""
    async with async_session() as session:
        async with session.begin():

            item_dal = ItemDAL(session)
            items = item_dal.get_all_items()
            return await items

@app.get("/get_articuls")
async def get_articuls():
    """
    return only articuls"""
    async with async_session() as session:
        async with session.begin():

            item_dal = ItemDAL(session)
            items = item_dal.get_articuls()
            return await items
@app.get("/get_item_by_articul")
async def get_item_by_articul(articul:str):
    async with async_session() as session:
        async with session.begin():

            item_dal = ItemDAL(session)
            item = item_dal.get_item_by_id(articul=articul)
            return await item

@app.get("/update_item_info")
async def update_item_unfo(articul:str):
    """
    update item info by articul"""
    await update_item_data(articul)




@app.on_event("startup")
async def startup():
    # create db tables
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    # await database.disconnect()
    pass


@app.get("/ping")
async def pong():
    return "pong!"
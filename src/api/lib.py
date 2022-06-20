import requests
from api.crud import ItemDAL
from api.models import StratChoice
from db import Base, async_session, engine


def get_price_wb(articul):
    try:
        url = f"https://card.wb.ru/cards/detail?spp=0&regions=68,64,83,4,38,80,33,70,82,86,75,30,69,22,66,31,48,1,40,71&pricemarginCoeff=1.0&reg=0&appType=1&emp=0&locale=ru&lang=ru&cur=rub&couponsGeo=12,3,18,15,21&dest=-1029256,-102269,-1278703,-1255563&nm={articul}"
        return requests.get(url).json()["data"]["products"][0]["salePriceU"] / 100
    except BaseException as BE:
        print(f"catched {BE}")
        return None


async def update_item_data(articul):

    wb_price = get_price_wb(articul)  # current price of item

    async with async_session() as session:
        async with session.begin():

            item_dal = ItemDAL(session)
            item = item_dal.get_item_by_id(articul=articul)
    c_item = await item

    participants_list_art = c_item[0].participants.split(", ")
    participants_list_price = [get_price_wb(i) for i in participants_list_art]

    new_price = None
    if any(participants_list_price):
        if c_item[0].strategy == StratChoice.AVERAGE:
            new_price = sum(participants_list_price) / len(participants_list_price)
        if c_item[0].strategy == StratChoice.EDLP:
            new_price = (
                min(participants_list_price) - min(participants_list_price) * 0.01
            )

    async with async_session() as session:
        async with session.begin():

            item_dal = ItemDAL(session)
            item = await item_dal.update_item(articul=articul, new_price=new_price)

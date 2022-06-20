import requests
from api.crud import ItemDAL
from db import Base, async_session, engine


def get_data_wb(art):
    url =  f"https://card.wb.ru/cards/detail?spp=0&regions=68,64,83,4,38,80,33,70,82,86,75,30,69,22,66,31,48,1,40,71&pricemarginCoeff=1.0&reg=0&appType=1&emp=0&locale=ru&lang=ru&cur=rub&couponsGeo=12,3,18,15,21&dest=-1029256,-102269,-1278703,-1255563&nm={art}"
    return requests.get(url).json()


async def update_item_data(art):

    # het current price WB

    wb_price = get_data_wb(art)["data"]["products"][0]["salePriceU"] / 100
    async with async_session() as session:
        async with session.begin():

            item_dal = ItemDAL(session)
            item = await item_dal.update_item(articul=art, new_price=wb_price)
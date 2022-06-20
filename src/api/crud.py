from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import update
from typing import List, Optional
from api.models import ItemStore, ItemSchema, ItemDB


class ItemDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def save_item(self, payload: ItemSchema) -> ItemDB:
        new_item = ItemStore(
            strategy=payload.strategy, 
            articul=payload.articul,
            participants=payload.participants
            )

        self.db_session.add(new_item)
        await self.db_session.flush()
        return new_item

    async def get_all_items(self) -> List[ItemStore]:
        """
        return list of all ItemStore objects"""
        q = await self.db_session.execute(select(ItemStore))
        return q.scalars().all()


    async def get_articuls(self):
        """
        return only list articuls"""
        q = await self.db_session.execute(select(ItemStore.articul))
        return [i[0] for i in q.all()]

    async def get_item_by_id(self, articul):
        q = await self.db_session.execute(select(ItemStore).where(ItemStore.articul==articul))
        return q.one()


    async def update_item(self, articul: str, participants: Optional[str] = None, participants_have: Optional[str]=None, new_price: Optional[int] = None):
        q = update(ItemStore).where(ItemStore.articul == articul)
        if participants:
            q = q.values(participants=participants)
        if participants_have:
            q = q.values(participants_have=participants_have)
        if new_price:
            q = q.values(new_price=new_price)
        print(q)
        q.execution_options(synchronize_session="fetch")

        await  self.db_session.execute(q)

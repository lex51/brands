from sqlalchemy import Column, String, DateTime, Enum, Boolean, Float
from sqlalchemy import func
import  enum


from db import Base

from pydantic import BaseModel

# SQLAlchemy

class StratChoice(enum.Enum):
    EDLP = "EDLP"
    AVERAGE = "AVERAGE"

class ItemStore(Base):
    __tablename__ = "Items"
    articul = Column(String, primary_key=True)
    strategy = Column(Enum(StratChoice))

    participants = Column(String)
    parse_date = Column(DateTime(timezone=True), server_default=func.now())
    participants_have = Column(Boolean)
    new_price = Column(Float)


from pydantic import Field


class ItemSchema(BaseModel):

    articul:str = Field()
    strategy:StratChoice = Field()
    participants:str = Field()



class ItemDB(ItemSchema):
    pass



class ItemDB(ItemSchema):
    id: int


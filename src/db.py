from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from sqlalchemy.engine import URL

from os import getenv as os_ge

SQLALCHEMY_DATABASE_URL = URL.create(
    "postgresql+asyncpg",
    username=os_ge("POSTGRES_USER"),
    password=os_ge("POSTGRES_PASSWORD"),
    host=os_ge("POSTGRES_HOST"),
    database=os_ge("POSTGRES_DB"),
)


engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

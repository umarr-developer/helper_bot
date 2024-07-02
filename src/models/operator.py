from datetime import datetime

from sqlalchemy import Column, Integer, Sequence, Date, insert, BigInteger, ForeignKey, select, String
from sqlalchemy.orm import sessionmaker

from src.service.database import Base


class Operator(Base):
    __tablename__ = 'operators'

    id = Column(Integer, Sequence('id'), primary_key=True)
    username = Column(String(length=255))
    user_id = Column(BigInteger, ForeignKey('users.user_id'))

    created_on = Column(Date, default=datetime.now)
    update_on = Column(Date, default=datetime.now, onupdate=datetime.now)

    @classmethod
    async def new(cls, db_session: sessionmaker, user_id: int):
        sql = insert(cls).values(user_id=user_id)
        async with db_session() as session:
            await session.execute(sql)
            await session.commit()

    @classmethod
    async def get(cls, db_session: sessionmaker, user_id: int) -> tuple['User']:
        sql = select(cls).where(cls.user_id == user_id)
        async with db_session() as session:
            response = await session.execute(sql)
        return response.fetchone()

    @classmethod
    async def all(cls, db_session: sessionmaker) -> list[tuple['User']]:
        sql = select(cls)
        async with db_session() as session:
            response = await session.execute(sql)
        return response.fetchall()

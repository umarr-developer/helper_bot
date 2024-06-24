from datetime import datetime

from sqlalchemy import (BigInteger, Boolean, Column, Date, Integer, Sequence,
                        insert, select, update)

from src.service.database import Base, sessionmaker


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('id'), unique=True)
    user_id = Column(BigInteger, primary_key=True)
    blocked = Column(Boolean, default=False)
    call_operator = Column(Boolean, default=True)
    send_ticket = Column(Boolean, default=True)

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
    async def block(cls, db_session: sessionmaker, user_id: int):
        sql = update(cls).where(cls.user_id == user_id).values(blocked=True)
        async with db_session() as session:
            await session.execute(sql)
            await session.commit()

    @classmethod
    async def unblock(cls, db_session: sessionmaker, user_id: int):
        sql = update(cls).where(cls.user_id == user_id).values(blocked=False)
        async with db_session() as session:
            await session.execute(sql)
            await session.commit()

    @classmethod
    async def block_call_operator(cls, db_session: sessionmaker, user_id: int):
        sql = update(cls).where(cls.user_id == user_id).values(call_operator=False)
        async with db_session() as session:
            await session.execute(sql)
            await session.commit()

    @classmethod
    async def unblock_call_operator(cls, db_session: sessionmaker, user_id: int):
        sql = update(cls).where(cls.user_id == user_id).values(call_operator=True)
        async with db_session() as session:
            await session.execute(sql)
            await session.commit()

    @classmethod
    async def block_send_ticket(cls, db_session: sessionmaker, user_id: int):
        sql = update(cls).where(cls.user_id == user_id).values(send_ticket=False)
        async with db_session() as session:
            await session.execute(sql)
            await session.commit()

    @classmethod
    async def unblock_send_ticket(cls, db_session: sessionmaker, user_id: int):
        sql = update(cls).where(cls.user_id == user_id).values(send_ticket=True)
        async with db_session() as session:
            await session.execute(sql)
            await session.commit()

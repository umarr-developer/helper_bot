from src.service.database import Base, sessionmaker
from sqlalchemy import Column, Integer, Boolean, Sequence, Text, insert, select


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, Sequence('id'), primary_key=True)
    question = Column(Text)
    answer = Column(Text)

    @classmethod
    async def new(cls, db_session: sessionmaker, question: str, answer: str):
        sql = insert(cls).values(question=question, answer=answer)
        async with db_session() as session:
            await session.execute(sql)
            await session.commit()

    @classmethod
    async def get(cls, db_session: sessionmaker, _id: int):
        sql = select(cls).where(cls.id == _id)
        async with db_session() as session:
            response = await session.execute(sql)
        return response.fetchone()
    
    @classmethod
    async def all(cls, db_session: sessionmaker):
        sql = select(cls)
        async with db_session() as session:
            response = await session.execute(sql)
        return response.fetchall()

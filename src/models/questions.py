from sqlalchemy import Column, Integer, Sequence, Text, insert, select, delete, update

from src.service.database import Base, sessionmaker


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
    async def get(cls, db_session: sessionmaker, _id: int) -> tuple['Question']:
        sql = select(cls).where(cls.id == _id)
        async with db_session() as session:
            response = await session.execute(sql)
        return response.fetchone()

    @classmethod
    async def all(cls, db_session: sessionmaker) -> list[tuple['Question']]:
        sql = select(cls)
        async with db_session() as session:
            response = await session.execute(sql)
        return response.fetchall()

    @classmethod
    async def delete(cls, db_session: sessionmaker, _id: int):
        sql = delete(cls).where(cls.id == _id)
        async with db_session() as session:
            await session.execute(sql)
            await session.commit()

    @classmethod
    async def edit_question(cls, db_session: sessionmaker, _id: int, question: str):
        sql = update(cls).where(cls.id == _id).values(question=question)
        print(_id, question)
        async with db_session() as session:
            await session.execute(sql)
            await session.commit()

    @classmethod
    async def edit_answer(cls, db_session: sessionmaker, _id: int, answer: str):
        sql = update(cls).where(cls.id == _id).values(answer=answer)
        async with db_session() as session:
            await session.execute(sql)
            await session.commit()

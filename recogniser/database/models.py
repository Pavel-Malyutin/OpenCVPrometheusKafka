from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.future import select

from recogniser.database.db_setup import Base, db


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    face = Column(String(5000), unique=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)

    @classmethod
    async def create(cls, **kwargs):
        user = cls(**kwargs)
        db.add(user)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return user

    @classmethod
    async def get(cls, user_id):
        query = select(cls).where(cls.id == user_id)
        users = await db.execute(query)
        (user,) = users.first()
        return user

    @classmethod
    async def get_all(cls):
        query = select(cls)
        users = await db.execute(query)
        users = users.scalars().all()
        return users

    @classmethod
    async def update(cls, user_id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == user_id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def delete(cls, user_id):
        query = sqlalchemy_delete(cls).where(cls.id == user_id)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return True

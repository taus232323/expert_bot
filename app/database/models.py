from sqlalchemy import BigInteger, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship, mapped_column, DeclarativeBase, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from settings import SQLALCHEMY_URL
from typing import List

engine = create_async_engine(SQLALCHEMY_URL, echo=True)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    username = mapped_column(String(50))
    
    participants_rel: Mapped[List['Participants']] = relationship(back_populates="user_rel")
    
class Contacts(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    contact_type: Mapped[str] = mapped_column(String(50))
    value: Mapped[str] = mapped_column(String(50))


class Cases(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1024))

class Services(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1024))

class Events(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1024))
    date: Mapped[DateTime] = mapped_column(DateTime)
    
    participants_rel: Mapped[List['Participants']] = relationship(back_populates="event_rel")

class Participants(Base):
    __tablename__ = "participants"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    event: Mapped[int] = mapped_column(ForeignKey("events.id"))
    
    user_rel: Mapped['Users'] = relationship(back_populates="participants_rel")
    event_rel: Mapped['Events'] = relationship(back_populates="participants_rel")

class Briefing(Base):
    __tablename__ = "briefing"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    question: Mapped[str] = mapped_column(String(1024))
    answer: Mapped[str] = mapped_column(String(200))
    
class Other(Base):
    __tablename__ = "other"

    id: Mapped[int] = mapped_column(primary_key=True)
    instructions: Mapped[str] = mapped_column(String(1024))
    welcome: Mapped[str] = mapped_column(String(1024))
    welcome_img: Mapped[str] = mapped_column(String(200))
  

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
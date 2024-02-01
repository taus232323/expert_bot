from sqlalchemy import BigInteger, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from settings import SQLALCHEMY_URL

engine = create_async_engine(SQLALCHEMY_URL, echo=True)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = mapped_column(BigInteger, primary_key=True)
    tg_id = mapped_column(BigInteger)
    username = mapped_column(String)
    first_name = mapped_column(String)
    last_name = mapped_column(String)
    
class Contacts(Base):
    __tablename__ = "contacts"

    id = mapped_column(BigInteger, primary_key=True)
    contact_type = mapped_column(String)
    phone = mapped_column(String)
    email = mapped_column(String)
    working_hours = mapped_column(String)
    holydays = mapped_column(String)
    office_address = mapped_column(String)
    website_links = relationship("WebsiteLink", back_populates="contact")

class WebsiteLinks(Base):
    __tablename__ = "website_links"

    id = mapped_column(BigInteger, primary_key=True)
    name = mapped_column(String)
    url = mapped_column(String)
    contact_id = mapped_column(ForeignKey("contacts.id"))

    contact = relationship("Contact", back_populates="website_links")

class Cases(Base):
    __tablename__ = "cases"

    id = mapped_column(BigInteger, primary_key=True)
    title = mapped_column(String)
    description = mapped_column(String)
    
class Events(Base):
    __tablename__ = "events"

    id = mapped_column(BigInteger, primary_key=True)
    name = mapped_column(String)
    description = mapped_column(String)
    date = mapped_column(DateTime)

class Services(Base):
    __tablename__ = "services"

    id = mapped_column(BigInteger, primary_key=True)
    name = mapped_column(String)
    description = mapped_column(String)

class Briefing(Base):
    __tablename__ = "briefing"

    id = mapped_column(BigInteger, primary_key=True)
    instructions = mapped_column(String)
    question = mapped_column(String)
    answer = mapped_column(String)
  

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
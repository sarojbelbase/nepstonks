from datetime import datetime
from os import path

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from const import DATABASE_URI

sqlite_db = 'sqlite:///' + path.join(DATABASE_URI)
connect_args = {'check_same_thread': False}
engine = create_engine(sqlite_db, echo=False, connect_args=connect_args)
session = Session(bind=engine)
BaseModel = declarative_base()


class Stock(BaseModel):
    __tablename__ = 'stock'
    id = Column(Integer(), primary_key=True)
    company_name = Column(String(), nullable=False)
    end_date = Column(Date(), nullable=False)
    investment_id = Column(Integer(), nullable=False)
    issued_by = Column(String(), nullable=False)
    pdf = Column(String(), nullable=True)
    ratio = Column(String(), nullable=True)
    start_date = Column(Date(), nullable=False)
    stock_id = Column(Integer(), nullable=False)
    stock_symbol = Column(String(), nullable=False)
    stock_type = Column(String(), nullable=False)
    units = Column(String(), nullable=True)
    is_published = Column(Boolean(), default=False)
    stock_added_at = Column(DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f'{self.company_name}({self.stock_type})'


class News(BaseModel):
    __tablename__ = 'news'
    id = Column(Integer(), primary_key=True)
    date_published = Column(DateTime(), nullable=False)
    description = Column(Text(), nullable=True)
    image_url = Column(String(), nullable=True)
    is_published = Column(Boolean(), default=False)
    lang = Column(String(), nullable=False)
    source = Column(String(), nullable=False)
    title = Column(String(), nullable=False)
    url = Column(String(), nullable=False)
    article_added_at = Column(DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f'{self.title}({self.source})'


# To create a new database with models specified above if db doesn't exist
if not path.isfile(DATABASE_URI):
    BaseModel.metadata.create_all(engine)

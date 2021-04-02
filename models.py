from const import DATABASE_URI
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from os import path

sqlite_db = 'sqlite:///' + path.join(DATABASE_URI)
engine = create_engine(sqlite_db, echo=True)
# connect_args = {'check_same_thread': False}
session = Session(bind=engine)
BaseModel = declarative_base()


class Stock(BaseModel):
    __tablename__ = 'stock'
    id = Column(Integer(), primary_key=True)
    share_id = Column(Integer())
    investment_id = Column(Integer())
    start_date = Column(DateTime())
    end_date = Column(DateTime())
    nep_start_date = Column(DateTime())
    nep_end_date = Column(DateTime())
    share_type = Column(String())
    company_name = Column(String())
    stock_symbol = Column(String())
    issued_by = Column(String())
    units = Column(String())
    pdf = Column(String())
    ratio = Column(String())


# To create database with given model if it doesn't exists
if not path.isfile(DATABASE_URI):
    BaseModel.metadata.create_all(engine)

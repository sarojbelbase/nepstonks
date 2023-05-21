from datetime import datetime
from os import path

from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey, Integer,
                        String, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

from utils.const import DATABASE_URI

sqlite_db = 'sqlite:///' + path.join(DATABASE_URI)
connect_args = {'check_same_thread': False}
engine = create_engine(sqlite_db, echo=False, connect_args=connect_args)
session = Session(bind=engine)
BaseModel = declarative_base()


class Stock(BaseModel):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    company_name = Column(String, nullable=False)
    stock_symbol = Column(String, nullable=False)
    share_registrar = Column(String, nullable=True)
    sector_name = Column(String, nullable=True)
    share_type = Column(String, nullable=True)
    price_per_unit = Column(Integer, nullable=True)
    rating = Column(String, nullable=True)
    units = Column(Integer, nullable=True)
    min_units = Column(Integer, nullable=True)
    max_units = Column(Integer, nullable=True)
    total_amount = Column(Integer, nullable=True)
    opening_date = Column(Date, nullable=True)
    closing_date = Column(Date, nullable=True)
    fiscal_year = Column(String, nullable=True)
    is_published = Column(Boolean(), default=False)
    stock_added_at = Column(DateTime(), default=datetime.utcnow)
    chat = relationship(
        'Telegram', backref='stock', uselist=False,
        lazy=True, cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'{self.company_name} announced {self.stock_symbol} on {self.opening_date}'


class Telegram(BaseModel):
    __tablename__ = 'telegram'
    id = Column(Integer(), primary_key=True)
    message_id = Column(Integer(), nullable=False)
    stock_id = Column(Integer(), ForeignKey('stock.id'))

    def __repr__(self):
        return f'Message: {self.message_id} Stock: {self.stock_id}'


class Announcement(BaseModel):
    __tablename__ = 'announcement'
    id = Column(Integer(), primary_key=True)
    content = Column(String(), nullable=False)
    content_url = Column(String(), nullable=True)
    published_date = Column(Date(), nullable=True)
    is_published = Column(Boolean(), default=False)
    scraped_at = Column(DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return self.content


# Map the models to the database as tables
BaseModel.metadata.create_all(engine, checkfirst=True)

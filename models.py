from datetime import datetime
from os import path

from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey, Integer,
                        String, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

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
    closing_date = Column(Date(), nullable=False)
    investment_id = Column(Integer(), nullable=False)
    issued_by = Column(String(), nullable=False)
    pdf_url = Column(String(), nullable=True)
    ratio = Column(String(), nullable=True)
    opening_date = Column(Date(), nullable=False)
    stock_id = Column(Integer(), nullable=False)
    scrip = Column(String(), nullable=False)
    stock_type = Column(String(), nullable=False)
    units = Column(String(), nullable=True)
    is_published = Column(Boolean(), default=False)
    stock_added_at = Column(DateTime(), default=datetime.utcnow)
    chat = relationship('Telegram', backref='stock', uselist=False,
                        lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.company_name}({self.stock_type})'


class Telegram(BaseModel):
    __tablename__ = 'telegram'
    id = Column(Integer(), primary_key=True)
    message_id = Column(Integer(), nullable=False)
    stock_id = Column(Integer(), ForeignKey('stock.id'))

    def __repr__(self):
        return f'Message: {self.message_id} Stock: {self.stock_id}'


if __name__ == '__main__':
    # To create a new database with models specified above if db doesn't exist
    if not path.isfile(DATABASE_URI):
        BaseModel.metadata.create_all(engine)

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///orders.db")


class OrderBook(Base):

    __tablename__ = "Consolidated Order Book"

    pairname = Column("pairname", String, primary_key=True)
    type = Column("type", String)
    price = Column("price", Integer)
    quantity = Column("quantity", Integer)
    exchange = Column("exchange",String)

order = OrderBook()



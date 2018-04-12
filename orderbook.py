from sqlalchemy import create_engine, Column, String, ForeignKey, Table, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()



class Order(Base):

    __tablename__ = "Order"

    pairname = Column("pairname", String, primary_key=True)
    type = Column("type", String, primary_key=True)
    price = Column("price", Float, primary_key=True)
    quantity = Column("quantity", Float, primary_key=True)
    exchange = Column("exchange",String, primary_key=True)


engine = create_engine("sqlite:///orders.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

def addGDAXSnapshot(snapshot):
    session = Session()
    tickers = snapshot['product_id']
    for order in snapshot["bids"]:
        gdaxOrder = Order()
        gdaxOrder.pairname = tickers
        gdaxOrder.type = "Bid"
        gdaxOrder.price = float(order[0])
        gdaxOrder.quantity = float(order[1])
        gdaxOrder.exchange = "GDAX"

        session.add(gdaxOrder)

    for order in snapshot["asks"]:
        gdaxOrder = Order()
        gdaxOrder.pairname = tickers
        gdaxOrder.type = "Ask"
        gdaxOrder.price = float(order[0])
        gdaxOrder.quantity = float(order[1])
        gdaxOrder.exchange = "GDAX"

        session.add(gdaxOrder)

    session.commit()
    session.close()





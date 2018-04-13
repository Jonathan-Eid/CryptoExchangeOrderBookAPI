from sqlalchemy import create_engine, Column, String, ForeignKey, Table, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import exc
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




def addOrder(order,session):
    try:
        session.add(order)
        session.commit()
    except exc.IntegrityError:
        session.rollback()

def addOrders(orders):
    session = Session()
    for o in orders:
        order = Order()
        order.pairname = o.pairname
        order.type = o.type
        order.price = o.price
        order.quantity = o.quantity
        order.exchange = o.exchange

        addOrder(order, session)

    session.close()

def addUpdates(queue):
    session = Session()
    while queue.empty() is False:
        o = queue.get()
        order = Order()

        order.pairname = o.pairname
        order.type = o.type
        order.price = o.price
        order.quantity = o.quantity
        order.exchange = o.exchange

        addOrder(order, session)

    session.close()


def printOrders():
    session = Session()
    orders = session.query(Order).all()
    for order in orders:
        print(order.price)
    session.close()



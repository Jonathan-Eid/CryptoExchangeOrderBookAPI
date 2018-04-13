from sqlalchemy import create_engine, Column, String, ForeignKey, Table, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import exc
import threading

from sqlalchemy.orm.events import SessionEvents

Base = declarative_base()

class Order(Base):

    __tablename__ = "Order"

    pairname = Column("pairname", String, primary_key=True)
    type = Column("type", String, primary_key=True)
    price = Column("price", Float, primary_key=True)
    quantity = Column("quantity", Float, primary_key=True)
    exchange = Column("exchange",String, primary_key=True)
    instance = Column("instance",String)


engine = create_engine("sqlite:///orders.db", echo=True)
Session = sessionmaker(bind=engine)


def init():
    Base.metadata.create_all(bind=engine)


def clear_data():
    session = Session()
    session.query(Order).delete()
    session.commit()
    session.close()
    Base.metadata.drop_all(bind=engine)


def addOrder(order,session):
    try:
        session.add(order)
        session.commit()
    except exc.IntegrityError:
        session.rollback()

def updateOrder(order,session):
    try:
        session.add(order)
        session.commit()
    except exc.IntegrityError:
        session.rollback()

def addOrders(orders):
    session = Session()
    session.autoflush = True
    for o in orders:
        order = Order()
        order.pairname = o.pairname
        order.type = o.type
        order.price = o.price
        order.quantity = o.quantity
        order.exchange = o.exchange
        order.instance = "snapshot"

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
        order.instance = "update"

        threading.Event().wait(0.1)

        addOrder(order, session)

        queue.task_done()


def printOrders():
    num=0
    session = Session()
    orders = session.query(Order).all()
    for order in orders:
        print(order.pairname,order.type,order.price,order.quantity,order.exchange,num)
        num+=1
    session.close()

def ordersGreaterThan(num):
    orders = []
    session = Session()

    order = session.query(Order).filter(Order.price > num)
    for o in order:
        orders.append(o)

    return orders

def ordersFromExchange(exch):
    orders = []
    session = Session()

    order = session.query(Order).filter(Order.exchange == exch)
    for o in order:
        orders.append(o)

    return orders
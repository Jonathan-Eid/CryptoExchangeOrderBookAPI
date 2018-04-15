from sqlalchemy import create_engine, Column, String, ForeignKey, Table, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy import exc
from queue import Queue
Base = declarative_base()

class Order(Base):

    __tablename__ = "Order"

    pairname = Column("pairname", String, primary_key=True)
    type = Column("type", String, primary_key=True)
    price = Column("price", Float, primary_key=True)
    quantity = Column("quantity", Float, primary_key=True)
    exchange = Column("exchange",String, primary_key=True)
    instance = Column("instance",String)


engine = create_engine("sqlite:///orders.db", echo=False)
Session = scoped_session(sessionmaker(bind=engine))
Base.metadata.create_all(bind=engine)


updateQ = Queue()

def clear_data():
    session = Session()
    session.query(Order).delete()
    session.commit()
    session.close()
    Base.metadata.drop_all(bind=engine)
    with updateQ.mutex:
        updateQ.queue.clear()


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
        update = session.query(Order).get((order.pairname,order.type,order.price,order.quantity,order.exchange))
        updateQ.put(update)
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
        order.instance = "snapshot"

        addOrder(order, session)
    Session.remove()


def addUpdates(o):
    session = Session()

    order = Order()

    order.pairname = o.pairname
    order.type = o.type
    order.price = o.price
    order.quantity = o.quantity
    order.exchange = o.exchange
    order.instance = "update"

    updateOrder(order, session)

    Session.remove()

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

def ordersFromPairname(tickers):
    orders = []
    session = Session()

    order = session.query(Order).filter(Order.pairname == tickers)
    for o in order:
        orders.append(o)

    return orders

def snapshotOrders():
    orders = []
    session = Session()

    order = session.query(Order).filter(Order.instance == "snapshot")
    for o in order:
        orders.append(o)

    return orders


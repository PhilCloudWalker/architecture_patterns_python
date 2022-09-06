import os
from sqlalchemy.orm import mapper, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Table, MetaData, create_engine
#import domain_package as model
from domain_package import OrderLine
from sqlalchemy.orm import sessionmaker


metadata = MetaData()

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True,  autoincrement=True),
)

def create_in_memory_session():
    engine = create_db('sqlite:///:memory:')
    return sessionmaker(bind=engine)()

def create_local_session():
    #file_path = f'{os.path.dirname(__file__)}/db.sqlite'
    file_path = f'alembicdb.sqlite'
    con_string = f'sqlite:///{file_path}'
    if not os.path.exists(file_path):
        create_db(con_string)
        print('db created')
    return sessionmaker(bind=create_engine(con_string))()

def create_db(con_string):
    engine = create_engine(con_string)
    metadata.create_all(engine)
    return engine


def create_session(connection_string=None, engine=None):
    if engine:
        return sessionmaker(bind=engine)()
    if connection_string:
        return sessionmaker(bind=create_engine(connection_string))()
    return None
    
def start_mappers():
    lines_mapper = mapper(OrderLine, order_lines)

if __name__ == '__main__':

    #session = create_in_memory_session()
    session = create_local_session()

    start_mappers()
    
    # How to create a session
    session.execute(
            "INSERT INTO order_lines (orderid, sku, qty) VALUES "
            '("order1", "RED-CHAIR", 12),'
            '("order1", "RED-TABLE", 13),'
            '("order2", "BLUE-LIPSTICK", 14)'
        )
    session.commit()
    res = session.query(OrderLine).all()
    
    print(res)
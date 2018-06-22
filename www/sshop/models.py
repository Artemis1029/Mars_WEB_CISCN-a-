import os
import string
import bcrypt
import random
from datetime import date

from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import FLOAT, VARCHAR, INTEGER
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import connect_str

BaseModel = declarative_base()
engine = create_engine(connect_str, echo=True, pool_recycle=3600)
db = scoped_session(sessionmaker(bind=engine))


class Commodity(BaseModel):
    __tablename__ = 'commoditys'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(200), unique=True, nullable=False)
    desc = Column(VARCHAR(500), default='no description')
    amount = Column(INTEGER, default=100)
    price = Column(FLOAT, nullable=False)
    def __repr__(self):
        return '<Commodity: %s>' % self.name

    def __price__(self):
        return self.price

# class Seckill(BaseModel):
#     __tablename__ = 'seckill'
#     id = Column(INTEGER, primary_key=True, autoincrement=True)
#     name = Column(VARCHAR(200), unique=True, nullable=False)
#     desc = Column(VARCHAR(500), default='no description')
#     amount = Column(INTEGER, default=2)
#     price = Column(FLOAT, nullable=False)



class User(BaseModel):
    __tablename__ = 'user'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(50))
    mail = Column(VARCHAR(50))
    password = Column(VARCHAR(60))
    integral = Column(FLOAT, default=100000000)
    in_shop = Column(VARCHAR(100), default="")
    cookies = Column(INTEGER, default=0)
    seckill = Column(INTEGER, default=1)
    def check(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf8'))

    def __repr__(self):
        return '<User: %s>' % self.username

    def pay(self, num):
        return (self.integral - num) if (self.integral - num) >= 0 else -1

    def check_login(self):
        return 1 if self.cookies else 0

    def __integral__(self):
        return self.integral


class Shopcar(BaseModel):
    __tablename__ ='shopcar'

    id = Column(INTEGER, primary_key=True, autoincrement=True)



if __name__ == "__main__":
    BaseModel.metadata.create_all(engine)
    name_ = ["YOU", "CAN", "GET", "THE", "FLAG", "IN", "MY", "DOCKER", "233s"]
    desc_ = "I don't know where is my flag!!!!!!!!!"
    desc_ = [i for i in desc_]
    for i in name_:
        name = ''.join([i])
        desc = ''.join(desc_)
        price = 20 #random.randint(10, 200)
        db.add(Commodity(name=name, desc=desc, price=price))
    # for i in range(10):
    #     db.add(Seckill(name="seckill flag" + str(i + 1), desc="it's not flag XD, my flag is in my docker", price=1, amount=2))
    db.commit()

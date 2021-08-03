from sqlalchemy import create_engine, Float, MetaData, Date, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from settings import user, password, host, port, database

database_dsn = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
#database_dsn = create_engine(f'postgresql://postgres:postgres@127.0.0.1:5432/food')
meta = MetaData()

Base = declarative_base()


class Food(Base):
    __tablename__ = "food"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    energy = Column(Float)
    protein = Column(Float)
    carbohydrate = Column(Float)
    fat = Column(Float)
    fiber = Column(Float)


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    weight = Column(Float)
    height = Column(Float)
    age = Column(Float)
    sex = Column(String)
    user = Column(Integer)


class Consumed(Base):
    __tablename__ = "consumed"
    id = Column(Integer, primary_key=True)
    product = Column(Integer, ForeignKey('food.id'))
    quantity = Column(Float)
    data = Column(Date)
    user = Column(Integer)
    food_type = Column(String)

from sqlalchemy import create_engine, Float, MetaData, Date, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

from settings import user, password, host, port, database

database_dsn = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
# database_dsn = create_engine(f'postgresql://postgres:postgres@127.0.0.1:5432/food')
meta = MetaData()

Base = declarative_base()


class Food(Base):
    __tablename__ = "food"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    energy = Column(Float)
    protein = Column(Float)
    carbohydrate = Column(Float)
    fiber = Column(Float)
    fat = Column(Float)
    food_group = Column(Float)
    alcohol = Column(Float)
    water = Column(Float)
    ash = Column(Float)
    trusted = Column(Boolean)
    added_by = Column(String)




class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    weight = Column(Float)
    height = Column(Float)
    age = Column(Float)
    sex = Column(String)
    user = Column(Integer)
    fname = Column(String)
    lname = Column(String)


class Consumed(Base):
    __tablename__ = "consumed"
    id = Column(Integer, primary_key=True)
    product = Column(Integer, ForeignKey('food.id'))
    quantity = Column(Float)
    data = Column(Date)
    user = Column(Integer)
    food_type = Column(String)


class FoodLang(Base):
    __tablename__ = "food_lang"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    foodid = Column(Integer, ForeignKey('food.id'))
    language = Column(String)

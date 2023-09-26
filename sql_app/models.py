from sqlalchemy import Column, String, Integer
from .database import Base


class Customer(Base):
    __tablename__ = "customers"

    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

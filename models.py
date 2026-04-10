from sqlalchemy import Column, Integer, String, Date, Time
from db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    phone = Column(String, unique=True)
    name = Column(String)

class Slot(Base):
    __tablename__ = "slots"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    status = Column(String, default="available")

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    phone = Column(String)
    date = Column(Date)
    time = Column(Time)
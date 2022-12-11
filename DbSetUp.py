# Import Dependencies
import sqlite3 as lite
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Float, DATETIME, NUMERIC
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import *
import datetime

# Create engine and automap_base
engine = create_engine('sqlite:///data/Neutrino.db', echo=True)
conn = engine.connect()

# Create Table SensorsData using SQLAchemy
Base = declarative_base()

class Sensors(Base):
    __tablename__ = 'SensorsData'

    id = Column(Integer, primary_key=True, autoincrement=True)
    TimeStamp = Column(DATETIME)
    Temperature = Column(NUMERIC)
    Gas = Column(NUMERIC)
    Humidity = Column(NUMERIC)
    Pressure = Column(NUMERIC)
    Altitude = Column(NUMERIC)
    Luminosity = Column(NUMERIC)

Base.metadata.create_all(conn)

# Creating dummy data set for test
# ----------------------------------
now = datetime.datetime.now()
test = Sensors(TimeStamp=(now),
               Temperature=75,
               Gas=100,
               Humidity=50,
               Pressure=1000,
               Altitude=1000,
               Luminosity=1000)

# Use sesion objec to comunicat to db
session = Session(bind=engine)

# Add test to the current session
session.add(test)

# Commit test to the database
session.commit()



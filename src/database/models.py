from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from src.database.db import engine

Base = declarative_base()


class Vessel(Base):
    __tablename__ = "vessel"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    mmsi = Column(String, nullable=False, unique=True)
    imo = Column(String, nullable=False, unique=True)
    country_iso = Column(String, default= None)
    country = Column(String, nullable=False)
    image = Column(String, default= None)
    ship_type = Column(String, default= None)
    type_specific = Column(String, default= None)
    navigational_status = Column(String, default= None)
    callsign = Column(String, default= None, unique=True)
    gross_tonnage = Column(String, default= None)
    teu = Column(String, default= '-')
    length = Column(String, default= None)
    beam = Column(String, default= None)
    year_of_built = Column(String, default= None)
    current_draught = Column(String, default= None)
    gas_m3 = Column(String, default= None)
    eni = Column(String, default= None)
    eta_utc = Column(String, default= None)
    draught = Column(String, default= None)
    deadweight = Column(String, default= None)
    speed = Column(String, default= None)
    atd_utc = Column(String, default= None)
    latitude = Column(String, default= None)
    longitude = Column(String, default= None)
    course = Column(String, default= None)
    destination = Column(String, default= None)
    last_port = Column(String, default= None)
    update_time = Column(DateTime, default=datetime.utcnow)

    async def create_table(self):
        """This function create this table in database."""
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


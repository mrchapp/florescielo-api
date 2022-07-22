from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship

from .database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(String, primary_key=True, index=True)
    owner = Column(String)
    type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)

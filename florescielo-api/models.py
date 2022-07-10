from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class DeviceLocation(Base):
    __tablename__ = "devices"

    id = Column(String, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)

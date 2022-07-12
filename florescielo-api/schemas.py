from typing import List

from pydantic import BaseModel


class FloresCieloDeviceInfo(BaseModel):
    DeviceID: str
    InfoVersion: int
    DeviceInfo: str


class FloresCieloTimesRequest(BaseModel):
    DeviceID: str
    TS: int


class FloresCieloStormData(BaseModel):
    Rain: int
    WindSpeed: int
    WindDirection: int
    RecordTS: int
    Voltage: int
    UV: int
    DebugInfo: str


class FloresCieloStormReport(BaseModel):
    Type: int
    DeviceID1: int
    DeviceID2: str
    VERSION1: str
    VERSION3: str
    VERSION3: str
    TS: int
    Data: List[FloresCieloStormData]

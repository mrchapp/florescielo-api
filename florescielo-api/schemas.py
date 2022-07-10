from pydantic import BaseModel


class FloresCieloTimesRequest(BaseModel):
    DeviceID: str
    TS: int


class FloresCieloDeviceInfo(BaseModel):
    DeviceID: str
    InfoVersion: int
    DeviceInfo: str

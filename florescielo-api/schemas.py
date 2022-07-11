from pydantic import BaseModel


class FloresCieloDeviceInfo(BaseModel):
    DeviceID: str
    InfoVersion: int
    DeviceInfo: str


class FloresCieloTimesRequest(BaseModel):
    DeviceID: str
    TS: int

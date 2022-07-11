import datetime
import json
from math import floor
from typing import List

import paho.mqtt.client as mqtt
from astral import LocationInfo
from astral.sun import sun
from fastapi import Depends, FastAPI, Header, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url=None, redoc_url=None)


def config_get(config, item):
    parts = item.split("/")
    return config[parts[0]][parts[1]]


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/devc/gettimeinfo2/")
def gettimeinfo(
    florescielo_request: schemas.FloresCieloTimesRequest, db: Session = Depends(get_db)
):
    print("# gettimeinfo2")

    device_location = crud.get_device_location(db, id=florescielo_request.DeviceID)
    if device_location:
        loc = LocationInfo(
            latitude=device_location.latitude, longitude=device_location.longitude
        )
    else:
        loc = LocationInfo(
            latitude=25.686186,
            longitude=-100.3168154,
        )

    timestamp = datetime.datetime.now(datetime.timezone.utc)

    s = sun(loc.observer, date=timestamp, tzinfo=loc.timezone)

    ret_data = {
        "ResponseValue": 200,
        "SunriseTime": floor(s["sunrise"].timestamp()),
        "SunsetTime": floor(s["sunset"].timestamp()),
        "TS": floor(timestamp.timestamp()),
    }

    print(ret_data)
    return ret_data


@app.post("/devc/postdeviceinfo/")
def postdeviceinfo(
    florescielo_deviceinfo: schemas.FloresCieloDeviceInfo, db: Session = Depends(get_db)
):
    print("# postdeviceinfo")

    timestamp = datetime.datetime.now(datetime.timezone.utc)

    ret_data = {
        "ResponseValue": 200,
        "TS": floor(timestamp.timestamp()),
    }

    print(ret_data)
    return ret_data


@app.post("/devc/skydevice/")
def skydevice(
    Info: str,
    db: Session = Depends(get_db),
):
    print("# skydevice")

    data = json.loads(Info)
    print(data)

    if mqtt_client:
        try:
            mqtt_client.connect(_mqtt_server, port=_mqtt_port, keepalive=30)
            device_id = data["DeviceID"].lower()
            topic_base = f"florescielo/{device_id}"
            for item in [
                "Temperature",
                "Humidity",
                "Voltage",
                "UVIndex",
                "Luminance",
                "Rain",
                "Pressure",
                "ChargerStatus",
                "TS",
            ]:
                topic_item = item.lower()
                topic = topic_base + "/" + topic_item
                mqtt_client.publish(topic, data[item])
        except ConnectionRefusedError as e:
            print("Unable to connect to MQTT server")

    timestamp = datetime.datetime.now(datetime.timezone.utc)

    ret_data = {
        "ResponseValue": 200,
        "TS": floor(timestamp.timestamp()),
    }

    print(ret_data)
    return ret_data


def mqtt_on_connect(client, userdata, flags, rc):
    # print("MQTT on_connect")
    pass


def mqtt_on_disconnect(client, userdata, rc):
    # print("MQTT on_disconnect")
    pass


def mqtt_on_publish(client, userdata, rc):
    # print("MQTT message published")
    pass


try:
    config_file = open("config.json")
    config = json.load(config_file)
except FileNotFoundError as e:
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="MissingConfig"
    )

# MQTT init
if "mqtt" in config:
    _mqtt_username = config_get(config, "mqtt/username")
    _mqtt_password = config_get(config, "mqtt/password")
    _mqtt_server = config_get(config, "mqtt/server")
    _mqtt_port = config_get(config, "mqtt/port")
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(_mqtt_username, password=_mqtt_password)
    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_disconnect = mqtt_on_disconnect
    mqtt_client.on_publish = mqtt_on_publish
    # client.on_message = mqtt_on_message

import datetime
import json
from math import floor
from os import makedirs, path

import paho.mqtt.client as mqtt
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import crud, helpers, models, responses, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url=None, redoc_url=None)


def config_get(config, item):
    parts = item.split("/")
    return config[parts[0]][parts[1]]


mqtt_config = {}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/devc/gettimeinfo2/", response_class=responses.CaseSensitiveHeadersResponse)
def gettimeinfo(
    florescielo_request: schemas.FloresCieloTimesRequest,
    db: Session = Depends(get_db),
):
    print("# gettimeinfo2")

    timestamp = datetime.datetime.now(datetime.timezone.utc)

    device_type = crud.get_device_type(db, id=florescielo_request.DeviceID)
    if device_type == "STORM":
        ret_data = {
            "ResponseValue": 200,
            "TS": floor(timestamp.timestamp()),
        }
        print(ret_data)
        return ret_data

    device_latitude, device_longitude = crud.get_device_location(
        db, id=florescielo_request.DeviceID
    )

    sunrise, sunset = helpers.get_sunrise_sunset(
        device_latitude, device_longitude, timestamp
    )

    ret_data = {
        "ResponseValue": 200,
        "SunriseTime": sunrise,
        "SunsetTime": sunset,
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
async def skydevice(
    Info: str,
    request: Request,
    db: Session = Depends(get_db),
):
    print("# skydevice")

    data = json.loads(Info)
    print(data)
    device_id = data["DeviceID"].lower()
    image = None
    timestamp = datetime.datetime.now(datetime.timezone.utc)

    if int(request.headers["content-length"]) > 0:
        image = await request.body()
        try:
            out_dir = "images"
            if not path.isdir(out_dir):
                makedirs(out_dir, mode=0o733)
            filename = device_id + "-" + str(int(timestamp.timestamp())) + ".jpg"
            with open(f"{out_dir}/{filename}", "wb") as f:
                f.write(image)
        except:
            print("WARNING: Could not save camera image.")

    if crud.device_db_store(db, device_id):
        helpers.db_store_sky_record(db, data, image)

    if mqtt_client:
        helpers.sky2mqtt(data, mqtt_client, mqtt_config)

    device_latitude, device_longitude = crud.get_device_location(db, id=device_id)

    sunrise, sunset = helpers.get_sunrise_sunset(
        device_latitude, device_longitude, timestamp
    )

    ret_data = {
        "ResponseValue": 200,
        "Message": 0,
        "SunsetTime": sunset,
        "TS": floor(timestamp.timestamp()),
        "SunriseTime": sunrise,
    }

    print(ret_data)
    return ret_data


@app.post(
    "/devc/uploadstormdata2/", response_class=responses.CaseSensitiveHeadersResponse
)
def uploadstormdata(
    storm_data: schemas.FloresCieloStormReport,
    db: Session = Depends(get_db),
):
    print("# uploadstormdata2")

    print(storm_data)
    timestamp = datetime.datetime.now(datetime.timezone.utc)
    device_id = storm_data.DeviceID2.lower()

    if crud.device_db_store(db, device_id):
        helpers.db_store_storm_record(db, storm_data)

    if mqtt_client:
        helpers.storm2mqtt(storm_data, mqtt_client, mqtt_config)

    ret_data = {"returnValue": 100, "TS": floor(timestamp.timestamp()), "message": 0}

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
    mqtt_config = {
        "username": config_get(config, "mqtt/username"),
        "password": config_get(config, "mqtt/password"),
        "server": config_get(config, "mqtt/server"),
        "port": config_get(config, "mqtt/port"),
    }

    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(
        mqtt_config["username"], password=mqtt_config["password"]
    )
    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_disconnect = mqtt_on_disconnect
    mqtt_client.on_publish = mqtt_on_publish
    # client.on_message = mqtt_on_message

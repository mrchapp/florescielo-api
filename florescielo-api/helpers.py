import datetime
from math import floor

from astral import LocationInfo
from astral.sun import sun
from timezonefinder import TimezoneFinder

from . import crud, models


def db_store_sky_record(db, data, image):
    device_id = data["DeviceID"].lower()
    timestamp = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

    sky_record = models.SkyRecord(
        device_id=device_id,
        timestamp=timestamp,
        temperature=data["Temperature"],
        humidity=data["Humidity"],
        voltage=data["Voltage"],
        uvindex=data["UVIndex"],
        luminance=data["Luminance"],
        rain=data["Rain"],
        pressure=data["Pressure"],
        charger_status=data["ChargerStatus"],
    )

    crud.device_db_store_sky(db, sky_record)


def db_store_storm_record(db, storm_data):
    device_id = storm_data.DeviceID2.lower()
    timestamp = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

    storm_record = models.StormRecord(
        device_id=device_id,
        timestamp=timestamp,
        rain=storm_data.Data[0].dict()["Rain"],
        uv=storm_data.Data[0].dict()["UV"],
        voltage=storm_data.Data[0].dict()["Voltage"],
        wind_direction=storm_data.Data[0].dict()["WindDirection"],
        wind_speed=storm_data.Data[0].dict()["WindSpeed"],
        debug_info=storm_data.Data[0].dict()["DebugInfo"],
    )

    crud.device_db_store_storm(db, storm_record)


def sky2mqtt(data, mqtt_client, mqtt_config):
    device_id = data["DeviceID"].lower()

    try:
        mqtt_client.connect(
            mqtt_config["server"], port=mqtt_config["port"], keepalive=30
        )
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


def storm2mqtt(storm_data, mqtt_client, mqtt_config):
    try:
        mqtt_client.connect(
            mqtt_config["server"], port=mqtt_config["port"], keepalive=30
        )
        device_id = storm_data.DeviceID2.lower()
        topic_base = f"florescielo/{device_id}"
        for item in [
            "Rain",
            "UV",
            "Voltage",
            "WindDirection",
            "WindSpeed",
        ]:
            topic_item = item.lower()
            topic = topic_base + "/" + topic_item
            mqtt_client.publish(topic, storm_data.Data[0].dict()[item])
    except ConnectionRefusedError as e:
        print("Unable to connect to MQTT server")


def get_sunrise_sunset(
    latitude,
    longitude,
    timestamp=datetime.datetime.now(datetime.timezone.utc),
):
    if latitude and longitude:
        tf = TimezoneFinder()
        tz = tf.timezone_at(lat=latitude, lng=longitude)
        loc = LocationInfo(latitude=latitude, longitude=longitude, timezone=tz)
    else:
        loc = LocationInfo(
            latitude=25.686186, longitude=-100.3168154, timezone="America/Monterrey"
        )

    s = sun(loc.observer, date=timestamp, tzinfo=loc.timezone)

    sunrise = floor(s["sunrise"].timestamp())
    sunset = floor(s["sunset"].timestamp())

    return sunrise, sunset

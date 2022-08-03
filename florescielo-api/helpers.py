import datetime
from math import floor

from astral import LocationInfo
from astral.sun import sun
from timezonefinder import TimezoneFinder

from . import crud


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

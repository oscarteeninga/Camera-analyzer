from enum import Enum

from flask_caching import Cache

config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
cache = Cache(config=config)


class Dictionaries(Enum):
    CAMERA_IP_TO_NAME = "CAMERA_IP_TO_NAME"
    CAMERA_NAME_TO_IP = "CAMERA_NAME_TO_IP"
    AREAS = "AREAS"

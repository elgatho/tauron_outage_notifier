"""Stałe integracji Tauron Outage Notifier."""
from datetime import timedelta

DOMAIN = "tauron_outage_notifier"
MANUFACTURER = "Tauron Outage Notifier"

API_BASE_URL = "https://www.tauron-dystrybucja.pl"
ENDPOINT_CITIES = "/waapi/enum/geo/cities"
ENDPOINT_STREETS = "/waapi/enum/geo/streets"
ENDPOINT_OUTAGES = "/waapi/outages/address"

CONF_CITY_NAME = "city_name"
CONF_CITY_GAID = "city_gaid"
CONF_STREET_NAME = "street_name"
CONF_STREET_GAID = "street_gaid"
CONF_HOUSE_NO = "house_no"
CONF_SCAN_INTERVAL = "scan_interval"

LOOKAHEAD = timedelta(days=30)
DEFAULT_SCAN_INTERVAL = 60
MIN_SCAN_INTERVAL = 15
MAX_SCAN_INTERVAL = 1440
MIN_SEARCH_LENGTH = 3

MAX_STATE_LENGTH = 255

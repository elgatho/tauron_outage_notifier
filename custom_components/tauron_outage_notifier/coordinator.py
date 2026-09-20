"""Data update coordinator for Tauron Outage Notifier."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .api import TauronApi, TauronApiError
from .const import (
    CONF_CITY_GAID,
    CONF_HOUSE_NO,
    CONF_STREET_NAME,
    CONF_SCAN_INTERVAL,
    CONF_STREET_GAID,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    LOOKAHEAD,
)

_LOGGER = logging.getLogger(__name__)


def _parse_date(value: str | None) -> Any:
    """Parse an API timestamp into an aware datetime."""
    if not value:
        return None
    return dt_util.parse_datetime(value)


def parse_outages(raw: dict[str, Any], street_name: str | None = None) -> list[dict[str, Any]]:
    """Normalise the API payload into a sorted list of outages.

    Only outages whose 'Message' field contains the given street name are kept.
    """
    outages = []
    for item in raw.get("OutageItems") or []:
        lokalizacja = item.get("Message", "")
        if street_name and isinstance(lokalizacja, str):
            if street_name.strip().lower() not in lokalizacja.strip().lower():
                continue
        elif street_name:
            continue
        start = _parse_date(item.get("StartDate"))
        end = _parse_date(item.get("EndDate"))
        outage_id = item.get("OutageId")
        outages.append(
            {
                "id": outage_id,
                "key": f"{outage_id}-{start.isoformat() if start else 'unknown'}",
                "message": item.get("Message"),
                "start": start,
                "end": end,
                "type_id": item.get("TypeId"),
                "is_active": bool(item.get("IsActive")),
                "lokalizacja": lokalizacja,
            }
        )
    outages.sort(key=lambda o: o["start"] or dt_util.utc_from_timestamp(0))
    return outages


class TauronOutageCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetches the outage list for one address."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        minutes = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} {entry.title}",
            update_interval=timedelta(minutes=minutes),
        )
        self.entry = entry
        self._api = TauronApi(async_get_clientsession(hass))
        self._seen_keys: set[str] | None = None

    async def _async_update_data(self) -> dict[str, Any]:
        now = dt_util.now()
        try:
            raw = await self._api.async_get_outages(
                city_gaid=self.entry.data[CONF_CITY_GAID],
                street_gaid=self.entry.data[CONF_STREET_GAID],
                house_no=self.entry.data[CONF_HOUSE_NO],
                from_date=now.strftime("%Y-%m-%dT%H:%M:%S"),
                to_date=(now + LOOKAHEAD).strftime("%Y-%m-%dT%H:%M:%S"),
            )
        except TauronApiError as err:
            raise UpdateFailed(str(err)) from err

        outages = parse_outages(raw, self.entry.data[CONF_STREET_NAME])

        current = next(
            (o for o in outages if o["start"] and o["end"] and o["start"] <= now <= o["end"]),
            None,
        )
        upcoming = next(
            (o for o in outages if o["start"] and o["start"] > now), None
        )

        if self._seen_keys is None:
            new_outages: list[dict[str, Any]] = []
        else:
            new_outages = [o for o in outages if o["key"] not in self._seen_keys]
        self._seen_keys = {o["key"] for o in outages}

        return {
            "outages": outages,
            "current": current,
            "next": upcoming,
            "new": new_outages,
        }

    async def async_fetch_range(
        self, start: Any, end: Any
    ) -> list[dict[str, Any]]:
        """Fetch outages for an arbitrary window (used by the calendar)."""
        try:
            raw = await self._api.async_get_outages(
                city_gaid=self.entry.data[CONF_CITY_GAID],
                street_gaid=self.entry.data[CONF_STREET_GAID],
                house_no=self.entry.data[CONF_HOUSE_NO],
                from_date=start.strftime("%Y-%m-%dT%H:%M:%S"),
                to_date=end.strftime("%Y-%m-%dT%H:%M:%S"),
            )
        except TauronApiError as err:
            raise UpdateFailed(str(err)) from err
        return parse_outages(raw, self.entry.data[CONF_STREET_NAME])

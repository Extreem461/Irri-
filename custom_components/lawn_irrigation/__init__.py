“”“The Lawn Irrigation System integration.”””
from **future** import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.event import async_track_time_interval
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import (
DOMAIN,
SERVICE_START_IRRIGATION,
SERVICE_STOP_IRRIGATION,
SERVICE_RUN_ZONE,
SERVICE_RUN_PROGRAM,
ATTR_ZONE_ID,
ATTR_DURATION,
ATTR_PROGRAM_NAME,
ATTR_ZONES,
DEFAULT_DURATION,
)
from .coordinator import LawnIrrigationCoordinator

_LOGGER = logging.getLogger(**name**)

PLATFORMS: list[Platform] = [Platform.SWITCH, Platform.SENSOR]

# Service schemas

SERVICE_START_IRRIGATION_SCHEMA = vol.Schema({
vol.Optional(ATTR_DURATION, default=DEFAULT_DURATION): cv.positive_int,
})

SERVICE_RUN_ZONE_SCHEMA = vol.Schema({
vol.Required(ATTR_ZONE_ID): cv.string,
vol.Optional(ATTR_DURATION, default=DEFAULT_DURATION): cv.positive_int,
})

SERVICE_RUN_PROGRAM_SCHEMA = vol.Schema({
vol.Required(ATTR_PROGRAM_NAME): cv.string,
vol.Optional(ATTR_ZONES): vol.All(cv.ensure_list, [cv.string]),
})

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
“”“Set up Lawn Irrigation System from a config entry.”””
coordinator = LawnIrrigationCoordinator(hass, entry)

```
await coordinator.async_config_entry_first_refresh()

hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

# Register services
await _async_register_services(hass, coordinator)

return True
```

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
“”“Unload a config entry.”””
unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

```
if unload_ok:
    coordinator = hass.data[DOMAIN].pop(entry.entry_id)
    coordinator.async_stop()

return unload_ok
```

async def _async_register_services(hass: HomeAssistant, coordinator: LawnIrrigationCoordinator) -> None:
“”“Register services for the integration.”””

```
async def start_irrigation(call: ServiceCall) -> None:
    """Start irrigation for all zones."""
    duration = call.data.get(ATTR_DURATION, DEFAULT_DURATION)
    await coordinator.async_start_irrigation(duration)

async def stop_irrigation(call: ServiceCall) -> None:
    """Stop all irrigation."""
    await coordinator.async_stop_irrigation()

async def run_zone(call: ServiceCall) -> None:
    """Run specific zone."""
    zone_id = call.data[ATTR_ZONE_ID]
    duration = call.data.get(ATTR_DURATION, DEFAULT_DURATION)
    await coordinator.async_run_zone(zone_id, duration)

async def run_program(call: ServiceCall) -> None:
    """Run irrigation program."""
    program_name = call.data[ATTR_PROGRAM_NAME]
    zones = call.data.get(ATTR_ZONES, [])
    await coordinator.async_run_program(program_name, zones)

# Register services
hass.services.async_register(
    DOMAIN, SERVICE_START_IRRIGATION, start_irrigation, SERVICE_START_IRRIGATION_SCHEMA
)
hass.services.async_register(
    DOMAIN, SERVICE_STOP_IRRIGATION, stop_irrigation
)
hass.services.async_register(
    DOMAIN, SERVICE_RUN_ZONE, run_zone, SERVICE_RUN_ZONE_SCHEMA
)
hass.services.async_register(
    DOMAIN, SERVICE_RUN_PROGRAM, run_program, SERVICE_RUN_PROGRAM_SCHEMA
)
```

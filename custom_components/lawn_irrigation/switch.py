“”“Switch platform for Lawn Irrigation System.”””
from **future** import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
DOMAIN,
CONF_ZONES,
CONF_ZONE_NAME,
CONF_ZONE_ENTITY,
CONF_ZONE_DURATION,
STATE_RUNNING,
STATE_IDLE,
)
from .coordinator import LawnIrrigationCoordinator

_LOGGER = logging.getLogger(**name**)

async def async_setup_entry(
hass: HomeAssistant,
config_entry: ConfigEntry,
async_add_entities: AddEntitiesCallback,
) -> None:
“”“Set up the lawn irrigation switch platform.”””
coordinator = hass.data[DOMAIN][config_entry.entry_id]

```
entities = []

# Add main system switch
entities.append(LawnIrrigationSystemSwitch(coordinator))

# Add individual zone switches
for zone in coordinator.zones:
    entities.append(LawnIrrigationZoneSwitch(coordinator, zone))

async_add_entities(entities, True)
```

class LawnIrrigationSystemSwitch(CoordinatorEntity, SwitchEntity):
“”“Main irrigation system switch.”””

```
def __init__(self, coordinator: LawnIrrigationCoordinator) -> None:
    """Initialize the switch."""
    super().__init__(coordinator)
    self._attr_name = f"{coordinator.entry.title} System"
    self._attr_unique_id = f"{coordinator.entry.entry_id}_system"
    self._attr_icon = "mdi:sprinkler"

@property
def is_on(self) -> bool:
    """Return if the system is on."""
    return self.coordinator.system_state == STATE_RUNNING

@property
def available(self) -> bool:
    """Return if entity is available."""
    return self.coordinator.last_update_success

@property
def extra_state_attributes(self) -> dict[str, Any]:
    """Return additional state attributes."""
    attrs = {
        "system_state": self.coordinator.system_state,
        "active_zones": self.coordinator.active_zones,
        "current_zone": self.coordinator.current_zone,
        "current_program": self.coordinator.current_program,
        "queue_length": len(self.coordinator.zone_queue),
    }
    
    if self.coordinator.start_time:
        attrs["start_time"] = self.coordinator.start_time.isoformat()
    
    if self.coordinator.total_duration:
        attrs["total_duration"] = self.coordinator.total_duration
    
    return attrs

async def async_turn_on(self, **kwargs: Any) -> None:
    """Turn on the irrigation system."""
    await self.coordinator.async_start_irrigation()

async def async_turn_off(self, **kwargs: Any) -> None:
    """Turn off the irrigation system."""
    await self.coordinator.async_stop_irrigation()
```

class LawnIrrigationZoneSwitch(CoordinatorEntity, SwitchEntity):
“”“Individual zone switch.”””

```
def __init__(self, coordinator: LawnIrrigationCoordinator, zone: dict) -> None:
    """Initialize the zone switch."""
    super().__init__(coordinator)
    self._zone = zone
    self._zone_name = zone[CONF_ZONE_NAME]
    self._zone_entity = zone[CONF_ZONE_ENTITY]
    self._zone_duration = zone[CONF_ZONE_DURATION]
    
    self._attr_name = f"{coordinator.entry.title} {self._zone_name}"
    self._attr_unique_id = f"{coordinator.entry.entry_id}_zone_{self._zone_name}"
    self._attr_icon = "mdi:sprinkler-variant"

@property
def is_on(self) -> bool:
    """Return if the zone is on."""
    return self._zone_entity in self.coordinator.active_zones

@property
def available(self) -> bool:
    """Return if entity is available."""
    # Check if underlying switch entity is available
    underlying_state = self.hass.states.get(self._zone_entity)
    return (
        self.coordinator.last_update_success
        and underlying_state is not None
        and underlying_state.state != "unavailable"
    )

@property
def extra_state_attributes(self) -> dict[str, Any]:
    """Return additional state attributes."""
    attrs = {
        "zone_name": self._zone_name,
        "zone_entity": self._zone_entity,
        "zone_duration": self._zone_duration,
        "is_running": self.is_on,
    }
    
    # Add underlying switch state
    underlying_state = self.hass.states.get(self._zone_entity)
    if underlying_state:
        attrs["underlying_state"] = underlying_state.state
    
    return attrs

async def async_turn_on(self, **kwargs: Any) -> None:
    """Turn on the zone."""
    await self.coordinator.async_run_zone(self._zone_name, self._zone_duration)

async def async_turn_off(self, **kwargs: Any) -> None:
    """Turn off the zone."""
    # Cancel the zone timer if it exists
    if self._zone_name in self.coordinator.zone_timers:
        self.coordinator.zone_timers[self._zone_name].cancel()
        del self.coordinator.zone_timers[self._zone_name]
    
    # Turn off the underlying switch
    await self.hass.services.async_call(
        "switch", "turn_off", {"entity
```

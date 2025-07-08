“”“Sensor platform for Lawn Irrigation System.”””
from **future** import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util.dt import utcnow

from .const import DOMAIN, STATE_RUNNING, STATE_IDLE
from .coordinator import LawnIrrigationCoordinator

_LOGGER = logging.getLogger(**name**)

async def async_setup_entry(
hass: HomeAssistant,
config_entry: ConfigEntry,
async_add_entities: AddEntitiesCallback,
) -> None:
“”“Set up the lawn irrigation sensor platform.”””
coordinator = hass.data[DOMAIN][config_entry.entry_id]

```
entities = [
    LawnIrrigationStateSensor(coordinator),
    LawnIrrigationRemainingTimeSensor(coordinator),
    LawnIrrigationActiveZonesSensor(coordinator),
]

async_add_entities(entities, True)
```

class LawnIrrigationStateSensor(CoordinatorEntity, SensorEntity):
“”“Sensor for irrigation system state.”””

```
def __init__(self, coordinator: LawnIrrigationCoordinator) -> None:
    """Initialize the sensor."""
    super().__init__(coordinator)
    self._attr_name = f"{coordinator.entry.title} State"
    self._attr_unique_id = f"{coordinator.entry.entry_id}_state"
    self._attr_icon = "mdi:information-outline"

@property
def native_value(self) -> str:
    """Return the state of the sensor."""
    return self.coordinator.system_state

@property
def extra_state_attributes(self) -> dict[str, Any]:
    """Return additional state attributes."""
    attrs = {
        "current_zone": self.coordinator.current_zone,
        "current_program": self.coordinator.current_program,
        "active_zones_count": len(self.coordinator.active_zones),
        "queue_length": len(self.coordinator.zone_queue),
    }
    
    if self.coordinator.start_time:
        attrs["start_time"] = self.coordinator.start_time.isoformat()
    
    return attrs
```

class LawnIrrigationRemainingTimeSensor(CoordinatorEntity, SensorEntity):
“”“Sensor for remaining irrigation time.”””

```
def __init__(self, coordinator: LawnIrrigationCoordinator) -> None:
    """Initialize the sensor."""
    super().__init__(coordinator)
    self._attr_name = f"{coordinator.entry.title} Remaining Time"
    self._attr_unique_id = f"{coordinator.entry.entry_id}_remaining_time"
    self._attr_icon = "mdi:timer-outline"
    self._attr_native_unit_of_measurement = "min"
    self._attr_device_class = SensorDeviceClass.DURATION

@property
def native_value(self) -> int:
    """Return the remaining time in minutes."""
    if self.coordinator.system_state != STATE_RUNNING:
        return 0
    
    # Calculate remaining time based on queue and current zone
    remaining = sum(duration for _, duration in self.coordinator.zone_queue)
    
    # Add remaining time from current zone if any
    if self.coordinator.current_zone and self.coordinator.start_time:
        elapsed = (utcnow() - self.coordinator.start_time).total_seconds() / 60
        current_zone_duration = next(
            (zone["zone_duration"] for zone in self.coordinator.zones 
             if zone["zone_name"] == self.coordinator.current_zone), 0
        )
        remaining += max(0, current_zone_duration - elapsed)
    
    return int(remaining)

@property
def extra_state_attributes(self) -> dict[str, Any]:
    """Return additional state attributes."""
    attrs = {
        "total_duration": self.coordinator.total_duration,
        "system_state": self.coordinator.system_state,
    }
    
    if self.coordinator.start_time:
        elapsed = (utcnow() - self.coordinator.start_time).total_seconds() / 60
        attrs["elapsed_time"] = int(elapsed)
    
    return attrs
```

class LawnIrrigationActiveZonesSensor(CoordinatorEntity, SensorEntity):
“”“Sensor for active zones count.”””

```
def __init__(self, coordinator: LawnIrrigationCoordinator) -> None:
    """Initialize the sensor."""
    super().__init__(coordinator)
    self._attr_name = f"{coordinator.entry.title} Active Zones"
    self._attr_unique_id = f"{coordinator.entry.entry_id}_active_zones"
    self._attr_icon = "mdi:sprinkler-variant"

@property
def native_value(self) -> int:
    """Return the number of active zones."""
    return len(self.coordinator.active_zones)

@property
def extra_state_attributes(self) -> dict[str, Any]:
    """Return additional state attributes."""
    return {
        "active_zone_entities": self.coordinator.active_zones,
        "current_zone": self.coordinator.current_zone,
        "total_zones": len(self.coordinator.zones),
        "queue_length": len(self.coordinator.zone_queue),
    }
```

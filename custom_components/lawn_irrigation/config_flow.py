“”“Config flow for Lawn Irrigation System integration.”””
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, CONF_ZONES, CONF_ZONE_NAME, CONF_ZONE_ENTITY, CONF_ZONE_DURATION

_LOGGER = logging.getLogger(**name**)

class LawnIrrigationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
“”“Handle a config flow for Lawn Irrigation System.”””

```
VERSION = 1

def __init__(self):
    """Initialize the config flow."""
    self.zones = []

async def async_step_user(self, user_input=None):
    """Handle the initial step."""
    if user_input is None:
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("system_name", default="Lawn Irrigation"): str,
            })
        )

    self.system_name = user_input["system_name"]
    return await self.async_step_zone()

async def async_step_zone(self, user_input=None):
    """Handle zone configuration."""
    errors = {}
    
    if user_input is not None:
        if user_input.get("add_zone"):
            zone_name = user_input.get("zone_name", "").strip()
            zone_entity = user_input.get("zone_entity", "").strip()
            zone_duration = user_input.get("zone_duration", 10)
            
            if not zone_name:
                errors["zone_name"] = "Zone name is required"
            elif not zone_entity:
                errors["zone_entity"] = "Zone entity is required"
            else:
                # Check if entity exists
                if zone_entity not in self.hass.states.async_entity_ids():
                    errors["zone_entity"] = "Entity not found"
                else:
                    self.zones.append({
                        CONF_ZONE_NAME: zone_name,
                        CONF_ZONE_ENTITY: zone_entity,
                        CONF_ZONE_DURATION: zone_duration
                    })
                    
                    # Clear form for next zone
                    user_input = {
                        "zone_name": "",
                        "zone_entity": "",
                        "zone_duration": 10,
                        "add_zone": False
                    }
        
        elif user_input.get("finish") and self.zones:
            return self.async_create_entry(
                title=self.system_name,
                data={
                    "system_name": self.system_name,
                    CONF_ZONES: self.zones
                }
            )
        elif user_input.get("finish") and not self.zones:
            errors["base"] = "At least one zone is required"

    # Get available switch entities
    switch_entities = [
        entity_id for entity_id in self.hass.states.async_entity_ids()
        if entity_id.startswith("switch.")
    ]

    data_schema = vol.Schema({
        vol.Optional("zone_name", default=""): str,
        vol.Optional("zone_entity", default=""): vol.In(switch_entities),
        vol.Optional("zone_duration", default=10): vol.All(vol.Coerce(int), vol.Range(min=1, max=120)),
        vol.Optional("add_zone", default=False): bool,
        vol.Optional("finish", default=False): bool,
    })

    return self.async_show_form(
        step_id="zone",
        data_schema=data_schema,
        errors=errors,
        description_placeholders={
            "zones_count": len(self.zones),
            "zones_list": ", ".join([zone[CONF_ZONE_NAME] for zone in self.zones])
        }
    )

@staticmethod
@callback
def async_get_options_flow(config_entry):
    """Get the options flow for this handler."""
    return LawnIrrigationOptionsFlow(config_entry)
```

class LawnIrrigationOptionsFlow(config_entries.OptionsFlow):
“”“Handle options flow for Lawn Irrigation System.”””

```
def __init__(self, config_entry):
    """Initialize options flow."""
    self.config_entry = config_entry

async def async_step_init(self, user_input=None):
    """Handle options flow."""
    if user_input is not None:
        return self.async_create_entry(title="", data=user_input)

    return self.async_show_form(
        step_id="init",
        data_schema=vol.Schema({
            vol.Optional(
                "default_duration",
                default=self.config_entry.options.get("default_duration", 10)
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=120)),
            vol.Optional(
                "enable_weather_check",
                default=self.config_entry.options.get("enable_weather_check", False)
            ): bool,
            vol.Optional(
                "rain_sensor_entity",
                default=self.config_entry.options.get("rain_sensor_entity", "")
            ): str,
        })
    )
```

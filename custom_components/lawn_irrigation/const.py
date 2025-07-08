"""Constants for the Lawn Irrigation System integration."""

DOMAIN = "lawn_irrigation"

# Configuration constants
CONF_ZONES = "zones"
CONF_ZONE_NAME = "zone_name"
CONF_ZONE_ENTITY = "zone_entity"
CONF_ZONE_DURATION = "zone_duration"

# Service constants
SERVICE_START_IRRIGATION = "start_irrigation"
SERVICE_STOP_IRRIGATION = "stop_irrigation"
SERVICE_RUN_ZONE = "run_zone"
SERVICE_RUN_PROGRAM = "run_program"

# Attributes
ATTR_ZONE_ID = "zone_id"
ATTR_DURATION = "duration"
ATTR_PROGRAM_NAME = "program_name"
ATTR_ZONES = "zones"

# States
STATE_IDLE = "idle"
STATE_RUNNING = "running"
STATE_PAUSED = "paused"

# Default values
DEFAULT_DURATION = 10
DEFAULT_SCAN_INTERVAL = 30

"""Constants for the frigidaire integration."""

DOMAIN = "frigidaire"
PLATFORMS = ["binary_sensor", "climate", "humidifier", "number", "sensor", "switch"]

# Keys must match SwitchDescription.key values in switch.py
SWITCH_OPTIONS: dict[str, str] = {
    "clean_air_mode": "Ionizer (Clean Air Mode)",
    "display_light": "Display Light",
    "ui_lock": "Child Lock",
}

# Keys must match diagnostic entity keys.
CONF_CHECK_FILTER_SENSOR = "check_filter"
CONF_FILTER_RUNTIME_SENSOR = "filter_runtime"

BINARY_SENSOR_OPTIONS: dict[str, str] = {
    CONF_CHECK_FILTER_SENSOR: "Check Filter",
}

SENSOR_OPTIONS: dict[str, str] = {
    CONF_FILTER_RUNTIME_SENSOR: "Filter Runtime",
}

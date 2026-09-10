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
CONF_BUCKET_STATUS_SENSOR = "bucket_status"
CONF_CHECK_FILTER_SENSOR = "check_filter"
CONF_COMPRESSOR_ESTIMATE = "compressor"
CONF_FILTER_RUNTIME_SENSOR = "filter_runtime"

DEFAULT_COOL_HYSTERESIS = 0.0
DEFAULT_COMPRESSOR_OFF_DELAY = 300
CONF_COOL_HYSTERESIS = "cool_hysteresis"
CONF_COMPRESSOR_OFF_DELAY = "compressor_off_delay"

BINARY_SENSOR_OPTIONS: dict[str, str] = {
    CONF_CHECK_FILTER_SENSOR: "Check Filter",
    CONF_BUCKET_STATUS_SENSOR: "Bucket Status",
}

SENSOR_OPTIONS: dict[str, str] = {
    CONF_FILTER_RUNTIME_SENSOR: "Filter Runtime",
}

"""My platform constants"""
from homeassistant.const import Platform

DOMAIN = "coway"

PLATFORMS = [
    Platform.FAN,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
]

IOCARE_FAN_OFF = "0"
IOCARE_FAN_LOW = "1"
IOCARE_FAN_MEDIUM = "2"
IOCARE_FAN_HIGH = "3"

IOCARE_TIMER_OFF = "0"
IOCARE_TIMER_1H = "60"
IOCARE_TIMER_2H = "120"
IOCARE_TIMER_4H = "240"
IOCARE_TIMER_8H = "480"

PRESET_MODE_AUTO = "Auto"
PRESET_MODE_NIGHT = "Night"

"""------------------for Refrigerator"""
import base64
import json
import logging
from typing import Optional

from . import (
    FEAT_ECOFRIENDLY,
    FEAT_EXPRESSMODE,
    FEAT_EXPRESSFRIDGE,
    FEAT_FRESHAIRFILTER,
    FEAT_ICEPLUS,
    FEAT_SMARTSAVINGMODE,
    FEAT_WATERFILTERUSED_MONTH,
)

from .device import (
    LABEL_BIT_OFF,
    LABEL_BIT_ON,
    STATE_OPTIONITEM_NONE,
    UNIT_TEMP_FAHRENHEIT,
    UNITTEMPMODES,
    Device,
    DeviceStatus,
)

FEATURE_DESCR = {
    "@RE_TERM_EXPRESS_FREEZE_W": "express_freeze",
    "@RE_TERM_EXPRESS_FRIDGE_W": "express_cool",
    "@RE_TERM_ICE_PLUS_W": "ice_plus",
}

REFRTEMPUNIT = {
    "Ｆ": UNITTEMPMODES.Fahrenheit,
    "℃": UNITTEMPMODES.Celsius,
    "˚F": UNITTEMPMODES.Fahrenheit,
    "˚C": UNITTEMPMODES.Celsius,
}

# REFRTEMPUNIT = {
#     "\uff26": UNITTEMPMODES.Fahrenheit,
#     "\u2103": UNITTEMPMODES.Celsius,
#     "\u02daF": UNITTEMPMODES.Fahrenheit,
#     "\u02daC": UNITTEMPMODES.Celsius,
# }

REFR_ROOT_DATA = "refState"
REFR_CTRL_BASIC = ["Control", "basicCtrl"]

REFR_STATE_ECO_FRIENDLY = ["EcoFriendly", "ecoFriendly"]
CMD_STATE_ECO_FRIENDLY = [REFR_CTRL_BASIC, ["SetControl", "basicCtrl"], REFR_STATE_ECO_FRIENDLY]

_LOGGER = logging.getLogger(__name__)


class RefrigeratorDevice(Device):
    """A higher-level interface for a dryer."""
    def __init__(self, client, device):
        super().__init__(client, device, RefrigeratorStatus(self, None))

    def _get_feature_info(self, item_key):
        config = self.model_info.config_value("visibleItems")
        if not config or not isinstance(config, list):
            return None
        if self.model_info.is_info_v2:
            feature_key = "feature"
        else:
            feature_key = "Feature"
        for item in config:
            feature_value = item.get(feature_key, "")
            if feature_value and feature_value == item_key:
                return item
        return None

    def _get_feature_title(self, item_key, def_value):
        item_info = self._get_feature_info(item_key)
        if not item_info:
            return None
        if self.model_info.is_info_v2:
            title_key = "monTitle"
        else:
            title_key = "Title"
        title_value = item_info.get(title_key)
        if not title_value:
            return def_value
        return FEATURE_DESCR.get(title_value, def_value)

    def _prepare_command_v1(self, cmd, key, value):
        """Prepare command for specific ThinQ1 device."""
        data_key = "value"
        if cmd.get(data_key, "") == "ControlData":
            data_key = "data"
        str_data = cmd.get(data_key)

        if str_data:
            status_data = self._status.data
            for dt_key, dt_value in status_data.items():
                if dt_key == key:
                    dt_value = value
                str_data = str_data.replace(f"{{{{{dt_key}}}}}", dt_value)
            _LOGGER.debug("Command data content: %s", str_data)
            if self.model_info.binary_control_data:
                cmd["format"] = "B64"
                str_list = json.loads(str_data)
                str_data = base64.b64encode(bytes(str_list)).decode("ascii")
            cmd[data_key] = str_data
        return cmd

    def _prepare_command_v2(self, cmd, key, value):
        """Prepare command for specific ThinQ2 device."""
        data_set = cmd.pop("data", None)
        if not data_set:
            return None

        for cmd_key, cmd_value in data_set[REFR_ROOT_DATA].items():
            if cmd_key == key:
                replace_item = value
            else:
                replace_item = "IGNORE"
            data_set[REFR_ROOT_DATA][cmd_key] = replace_item
        cmd["dataSetList"] = data_set

        return cmd

    def _prepare_command(self, ctrl_key, command, key, value):
        """Prepare command for specific device."""
        cmd = self.model_info.get_control_cmd(command, ctrl_key)
        if not cmd:
            return None

        if self.model_info.is_info_v2:
            return self._prepare_command_v2(cmd, key, value)
        return self._prepare_command_v1(cmd, key, value)

    def set_eco_friendly(self, turn_on=False):
        """Switch the echo friendly status."""

        status_key = self._get_state_key(REFR_STATE_ECO_FRIENDLY)
        status_name = LABEL_BIT_ON if turn_on else LABEL_BIT_OFF
        status_value = self.model_info.enum_value(status_key, status_name)
        if not status_value:
            return
        keys = self._get_cmd_keys(CMD_STATE_ECO_FRIENDLY)
        self.set(keys[0], keys[1], key=keys[2], value=status_value)
        self._status.update_status(status_key, status_value, True)

    def reset_status(self):
        self._status = RefrigeratorStatus(self, None)
        return self._status

    def poll(self) -> Optional["RefrigeratorStatus"]:
        """Poll the device's current state."""

        res = self.device_poll(REFR_ROOT_DATA)
        if not res:
            return None

        self._status = RefrigeratorStatus(self, res)
        return self._status


class RefrigeratorStatus(DeviceStatus):
    """Higher-level information about a refrigerator's current status.

    :param device: The Device instance.
    :param data: JSON data from the API.
    """
    def __init__(self, device, data):
        super().__init__(device, data)
        self._temp_unit = None
        self._eco_friendly_state = None
        self._sabbath_state = None

    def _get_eco_friendly_state(self):
        if self._eco_friendly_state is None:
            state = self.lookup_enum(["EcoFriendly", "ecoFriendly"])
            if not state:
                self._eco_friendly_state = ""
            else:
                self._eco_friendly_state = state
        return self._eco_friendly_state

    def _get_sabbath_state(self):
        if self._sabbath_state is None:
            state = self.lookup_enum(["Sabbath", "sabbathMode"])
            if not state:
                self._sabbath_state = ""
            else:
                self._sabbath_state = state
        return self._sabbath_state

    def _get_default_index(self, key_mode, key_index):
        config = self._device.model_info.config_value(key_mode)
        if not config or not isinstance(config, dict):
            return None
        return config.get(key_index)

    def _get_default_name_index(self, key_mode, key_index):
        index = self._get_default_index(key_mode, key_index)
        if index is None:
            return None
        return self._device.model_info.enum_index(key_index, index)

    def _get_default_temp_index(self, key_mode, key_index):
        config = self._get_default_index(key_mode, key_index)
        if not config or not isinstance(config, dict):
            return None
        unit = self._get_temp_unit()
        unit_key = "tempUnit_F" if unit == UNIT_TEMP_FAHRENHEIT else "tempUnit_C"
        return config.get(unit_key)

    def _get_temp_unit(self):
        if not self._temp_unit:
            temp_unit = self.lookup_enum(["TempUnit", "tempUnit"])
            if not temp_unit:
                self._temp_unit = STATE_OPTIONITEM_NONE
            else:
                self._temp_unit = (
                    REFRTEMPUNIT.get(temp_unit, UNITTEMPMODES.Celsius)
                ).value
        return self._temp_unit

    def _get_temp_val_v1(self, key):
        temp_key = None
        if self.eco_friendly_enabled:
            temp_key = self._get_default_temp_index("ecoFriendlyDefaultIndex", key)
        if temp_key is None:
            temp_key = self._data.get(key)
            if temp_key is None:
                return STATE_OPTIONITEM_NONE
        temp_key = str(temp_key)
        value_type = self._device.model_info.value_type(key)
        if value_type and value_type == "Enum":
            temp = self.lookup_enum(key)
            if not temp:
                return temp_key
            if temp != temp_key:
                return temp
        unit = self._get_temp_unit()
        unit_key = "_F" if unit == UNIT_TEMP_FAHRENHEIT else "_C"
        result = self._device.model_info.enum_name(
            key + unit_key, temp_key
        )
        if not result:
            return temp_key
        return result

    def _get_temp_val_v2(self, key):
        temp = None
        if self.eco_friendly_enabled:
            temp = self._get_default_temp_index("ecoFriendlyDefaultIndex", key)
        if temp is None:
            temp = self.int_or_none(self._data.get(key))
            if not temp:
                return STATE_OPTIONITEM_NONE
        temp = str(temp)

        unit = self._data.get("tempUnit")
        if not unit:
            return temp
        ref_key = self._device.model_info.target_key(
            key, unit, "tempUnit"
        )
        if not ref_key:
            return temp
        return self._device.model_info.enum_name(
            ref_key, temp
        )

    def update_status(self, key, value, upd_features=False):
        if not super().update_status(key, value):
            return False
        self._eco_friendly_state = None
        if upd_features:
            self._update_features()
        return True

    @property
    def is_on(self):
        return self.has_data

    @property
    def temp_refrigerator(self):
        if self.is_info_v2:
            return self._get_temp_val_v2("fridgeTemp")
        return self._get_temp_val_v1("TempRefrigerator")

    @property
    def temp_freezer(self):
        if self.is_info_v2:
            return self._get_temp_val_v2("freezerTemp")
        return self._get_temp_val_v1("TempFreezer")

    @property
    def temp_unit(self):
        return self._get_temp_unit()

    @property
    def door_opened_state(self):
        if self.is_info_v2:
            state = self._data.get("atLeastOneDoorOpen")
        else:
            state = self.lookup_enum("DoorOpenState")
        if not state:
            return STATE_OPTIONITEM_NONE
        return self._device.get_enum_text(state)

    @property
    def eco_friendly_enabled(self):
        state = self._get_eco_friendly_state()
        if not state:
            return False
        return True if state == LABEL_BIT_ON else False

    @property
    def eco_friendly_state(self):
        if self.is_info_v2:
            key = "ecoFriendly"
        else:
            key = "EcoFriendly"
        status = self._get_eco_friendly_state()
        return self._update_feature(
            key, status, True, FEAT_ECOFRIENDLY
        )

    @property
    def ice_plus_status(self):
        if self.is_info_v2:
            return None
        key = "IcePlus"
        status = self.lookup_enum(key)
        return self._update_feature(
            key, status, True, FEAT_ICEPLUS
        )

    @property
    def express_fridge_status(self):
        if not self.is_info_v2:
            return None
        key = "expressFridge"
        status = self.lookup_enum(key)
        return self._update_feature(
            key, status, True, FEAT_EXPRESSFRIDGE
        )

    @property
    def express_mode_status(self):
        if not self.is_info_v2:
            return None
        key = "expressMode"
        status = self.lookup_enum(key)
        return self._update_feature(
            key, status, True, FEAT_EXPRESSMODE
        )

    @property
    def smart_saving_state(self):
        state = self.lookup_enum(["SmartSavingModeStatus", "smartSavingRun"])
        if not state:
            return STATE_OPTIONITEM_NONE
        return self._device.get_enum_text(state)

    @property
    def smart_saving_mode(self):
        if self.is_info_v2:
            key = "smartSavingMode"
        else:
            key = "SmartSavingMode"
        status = self.lookup_enum(key)
        return self._update_feature(
            key, status, True, FEAT_SMARTSAVINGMODE
        )

    @property
    def fresh_air_filter_status(self):
        if self.is_info_v2:
            key = "freshAirFilter"
        else:
            key = "FreshAirFilter"
        status = self.lookup_enum(key)
        return self._update_feature(
            key, status, True, FEAT_FRESHAIRFILTER
        )

    @property
    def water_filter_used_month(self):
        if self.is_info_v2:
            key = "waterFilter"
        else:
            key = "WaterFilterUsedMonth"

        counter = None
        if self.is_info_v2:
            status = self._data.get(key)
            if status:
                counters = status.split("_", 1)
                if len(counters) > 1:
                    counter = counters[0]
        else:
            counter = self._data.get(key)
        value = "N/A" if not counter else counter
        return self._update_feature(
            key, value, False, FEAT_WATERFILTERUSED_MONTH
        )

    @property
    def locked_state(self):
        state = self.lookup_enum("LockingStatus")
        if not state:
            return STATE_OPTIONITEM_NONE
        return self._device.get_enum_text(state)

    @property
    def active_saving_status(self):
        return self._data.get("ActiveSavingStatus", "N/A")

    def _update_features(self):
        result = [
            self.eco_friendly_state,
            self.ice_plus_status,
            self.express_fridge_status,
            self.express_mode_status,
            self.smart_saving_mode,
            self.fresh_air_filter_status,
            self.water_filter_used_month,
        ]

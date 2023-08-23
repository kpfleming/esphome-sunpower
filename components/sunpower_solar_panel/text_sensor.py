import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components.sunpower_solar_pvs.text_sensor import (
    HARDWARE_VERSION_SCHEMA,
    SOFTWARE_VERSION_SCHEMA,
    hardware_version_to_code,
    software_version_to_code,
)
from . import CONF_PANEL_ID, Panel

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(CONF_PANEL_ID): cv.use_id(Panel),
        }
    )
    .extend(HARDWARE_VERSION_SCHEMA)
    .extend(SOFTWARE_VERSION_SCHEMA)
)


async def to_code(config):
    panel = await cg.get_variable(config[CONF_PANEL_ID])
    await hardware_version_to_code(panel, config)
    await software_version_to_code(panel, config)

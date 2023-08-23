import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components.sunpower_solar_pvs.text_sensor import (
    HARDWARE_VERSION_SCHEMA,
    SOFTWARE_VERSION_SCHEMA,
    hardware_version_to_code,
    software_version_to_code,
)
from . import Panel

CONFIG_SCHEMA = cv.Schema(
    {
        cv.use_id(Panel): HARDWARE_VERSION_SCHEMA.extend(SOFTWARE_VERSION_SCHEMA),
    }
)


async def to_code(config):
    for panel_id, panel_config in config.items():
        panel = await cg.get_variable(panel_id)

        await hardware_version_to_code(panel, panel_config)
        await software_version_to_code(panel, panel_config)

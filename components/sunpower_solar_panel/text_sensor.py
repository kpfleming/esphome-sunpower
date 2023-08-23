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
    for k, v in config.items():
        if k == "platform":
            continue

        panel = await cg.get_variable(k)

        await hardware_version_to_code(panel, v)
        await software_version_to_code(panel, v)

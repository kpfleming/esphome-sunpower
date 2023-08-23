import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components.sunpower_solar_pvs.binary_sensor import (
    ERROR_CONDITION_SCHEMA,
    error_condition_to_code,
)
from . import Panel

CONFIG_SCHEMA = cv.Schema(
    {
        cv.use_id(Panel): ERROR_CONDITION_SCHEMA,
    }
)


async def to_code(config):
    for panel_id, panel_config in config.items():
        panel = await cg.get_variable(panel_id)

        await error_condition_to_code(panel, panel_config)

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components.sunpower_solar_pvs.binary_sensor import (
    ERROR_CONDITION_SCHEMA,
    error_condition_to_code,
)
from . import CONF_PANEL_ID, Panel

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_PANEL_ID): cv.use_id(Panel),
    }
).extend(ERROR_CONDITION_SCHEMA)


async def to_code(config):
    panel = await cg.get_variable(config[CONF_PANEL_ID])
    await error_condition_to_code(panel, config)

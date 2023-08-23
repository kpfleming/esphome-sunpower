import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import (
    CONF_ID,
    CONF_NAME,
)
from esphome.components.sunpower_solar_pvs import (
    CONF_SUNPOWER_SOLAR_ID,
    sunpower_solar_ns,
    SunpowerSolar,
)
from esphome.components.sunpower_solar_panel import CONF_PANELS, Panel

CODEOWNERS = ["@kpfleming"]

Array = sunpower_solar_ns.struct("Array")

CONFIG_SCHEMA = cv.ensure_list(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(Array),
            cv.GenerateID(CONF_SUNPOWER_SOLAR_ID): cv.use_id(SunpowerSolar),
            cv.Optional(CONF_NAME): cv.string_strict,
            cv.Required(CONF_PANELS): cv.ensure_list(cv.use_id(Panel)),
        }
    )
)


async def to_code(config):
    for array in config:
        a = cg.new_Pvariable(array[CONF_ID])

        for panel in array[CONF_PANELS]:
            p = await cg.get_variable(panel)
            cg.add(a.add_panel(p))

        var = await cg.get_variable(array[CONF_SUNPOWER_SOLAR_ID])
        cg.add(var.add_array(a))

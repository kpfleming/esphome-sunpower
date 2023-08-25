import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import (
    CONF_ID,
    CONF_NAME,
)
from esphome.components.sunpower_solar_pvs import (
    CONF_SERIAL,
    CONF_SUNPOWER_SOLAR_ID,
    sunpower_solar_ns,
    SunpowerSolar,
)

CODEOWNERS = ["@kpfleming"]

Panel = sunpower_solar_ns.struct("Panel")

CONF_PANELS = "panels"

CONFIG_SCHEMA = cv.ensure_list(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(Panel),
            cv.GenerateID(CONF_SUNPOWER_SOLAR_ID): cv.use_id(SunpowerSolar),
            cv.Optional(CONF_NAME): cv.string_strict,
            cv.Required(CONF_SERIAL): cv.string_strict,
        }
    )
)


async def to_code(config):
    for panel in config:
        p = cg.new_Pvariable(panel[CONF_ID])

        cg.add(p.set_name(panel[CONF_NAME]))
        cg.add(p.set_serial(panel[CONF_SERIAL]))

        var = await cg.get_variable(panel[CONF_SUNPOWER_SOLAR_ID])
        cg.add(var.add_device(p))
